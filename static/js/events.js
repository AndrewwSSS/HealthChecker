const SUCCESSES_ICON = '<i class="bi bi-check-circle-fill"></i>'
const ERROR_ICON = '<i class="bi bi-x-circle-fill"></i>'
const TOAST_SHOW_DURATION = 1000
const FAIL_CALLBACK = () => {
    show_toast(`Fail to do operation`, "error")
}


function set_echart_data(id, data) {
    let chart_dom = document.getElementById(id)
    let chart = echarts.getInstanceByDom(chart_dom)
    chart.setOption({
        series: [{
            data: data
        }]
    })
    chart.resize()
}

function init_trainings_type_ratio_echart_callback(response) {
    echarts.init(document.querySelector("#training-types-ratio")).setOption({
        tooltip: {
            trigger: 'item'
        },
        legend: {
            top: '5%',
            left: 'center'
        },
        series: [{
            name: 'Access From',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '18',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: response['data']
        }]
    })
}

function init_PFC_ratio_echart_callback(response) {
    echarts.init(document.querySelector("#PFC-ratio")).setOption({
        tooltip: {
            trigger: 'item'
        },
        legend: {
            top: '5%',
            left: 'center'
        },
        series: [{
            name: 'Access From',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '18',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: response['data']
        }]
    })
}

function show_toast(msg, type = "success") {
    let toast = document.createElement('div')
    toast.classList.add("toastElement");
    let toastBox = document.getElementById("toastBox");
    toastBox.appendChild(toast);

    if(type === "success") {
        toast.classList.add("success");
        toast.innerHTML = SUCCESSES_ICON + msg
    }
    else if (type === "error") {
        toast.classList.add("error");
        toast.innerHTML = ERROR_ICON + msg
    }

    setTimeout(function () {
        toast.remove();
    },TOAST_SHOW_DURATION);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function ajax_post(url, data, done_callback, fail_callback, method = "POST") {
    $.ajax({
        type: method,
        url: url,
        data: data,
        dataType: "json",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
    }).done(done_callback).fail(fail_callback);
}


function ajax_get(url, data_string, done_callback, fail_callback, dataType = "json") {
    $.ajax({
        type: 'GET',
        url: url,
        data: data_string,
        dataType: dataType,
    }).done(done_callback).fail(fail_callback);
}

const select = (el, all = false) => {
    el = el.trim()
    if (all) {
        return [...document.querySelectorAll(el)]
    } else {
        return document.querySelector(el)
    }
}

const on = (type, el, listener, all = false) => {
    if (all) {
        let elements = select(el, all)
        if (elements.length > 0) {
            elements.forEach(e => e.addEventListener(type, listener))
        }
    } else {
        let element = select(el, all)
        if (element) {
            element.addEventListener(type, listener)
        }
    }
}

const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
}

function delete_training(event) {
    event.preventDefault();
    let training_element = event.target.parentElement.parentElement.parentElement
    let trainings_container = training_element.parentElement
    let formData = get_training_information(training_element)


    let success_callback = response => {
        training_element.remove()
        if (trainings_container.querySelectorAll("div").length === 0) {
            trainings_container.innerHTML = "<h6 class='card-title'>No trainings yet</h6>"
        }
        show_toast("Successfully deleted training", "success")
    }

    let endpoint = ""
    switch (formData.type) {
        case "PW":
            endpoint = "power-trainings"
            break
        case "WK":
            endpoint = "walking"
            break
        case "JG":
            endpoint = "jogging"
            break
        case "CY":
            endpoint = "cycling"
            break
        case "SW":
            endpoint = "swimming"
            break
    }
    ajax_post(
        `/api/${endpoint}/${formData.id}`,
        null,
        success_callback,
        FAIL_CALLBACK,
        "DELETE"
    )

}

function create_approach_form(event) {
    let elem = event.target.parentElement.parentElement.parentElement;
    let list_group = elem.querySelector(".list-group");

    let li = document.createElement("li");
    li.classList.add("list-group-item");
    li.innerHTML = `<div class="d-flex">
                      <div class="card-title-container gap-2 justify-content-between">
                          <span>Weight</span>
                          <input type="number" class="form-control" name="weight"/>
                          <span>Repeats</span>
                          <input type="number" class="form-control" name="repeats"/>
                          <button class="btn btn-primary saveApproach">Save</button>
                         <i class="bi bi-x-circle-fill deleteApproach deleteIcon"></i>
                      </div>
                    </div>`
    list_group.appendChild(li);
    li.querySelector(".saveApproach").addEventListener("click", create_or_update_approach);
    li.querySelector(".deleteApproach").addEventListener("click", delete_approach);

}

function create_or_update_approach(event) {
    let li_item = event.target.parentElement.parentElement.parentElement
    let formData = {
        weight: li_item.querySelector("input[name='weight']").value,
        repeats: li_item.querySelector("input[name='repeats']").value,
        training: li_item.parentElement.parentElement.getAttribute("data-exercise-id"),
    }
    if (li_item.hasAttribute("data-approach-id")) {
        let id = li_item.getAttribute("data-approach-id")

        let done_callback = response => show_toast("Approach successfully added.", "success")

        ajax_post(
            `/api/approaches/${id}/`,
            formData,
            done_callback,
            FAIL_CALLBACK,
            "PUT"
        )
    } else {
        let done_callback = response => {
            event.target.textContent = "Update"
            li_item.setAttribute("data-approach-id", response["id"]);
            show_toast("Approach successfully added.", "success")
        }

        ajax_post("/api/approaches/", formData, done_callback, FAIL_CALLBACK)
    }
}

function create_power_exercise() {
    let select_item = document.getElementById("select_exercise")

    let formData = {
        power_training: document.getElementById("training_id").getAttribute("value"),
        exercise: select_item.options[select_item.selectedIndex].value,
    }

    let done_callback = response => {
        let exercise_container = document.getElementById("exercise-container")
        let exercise_name = select_item.options[select_item.selectedIndex].text

        let noExerciseMessage = document.getElementById("no-exercises-message")
        if (noExerciseMessage)
            noExerciseMessage.remove()

        let div = document.createElement("div")
        div.setAttribute("data-exercise-id", `${response["id"]}`)
        div.innerHTML = (`<div class="card-title-container mb-3">
                              <div class="d-flex gap-3">
                                  <span>${exercise_name}</span>
                                  <i class="fa-solid fa-plus addApproach create-icon"></i>
                               </div>
                              <div class="card-title-container gap-2">
                                <i class="fa-solid fa-xmark delete-element-icon delete-exercise"></i>
                              </div>
                          </div>
                          <ul class="list-group mb-3"></ul>`)
        exercise_container.appendChild(div)
        on("click", ".addApproach", create_approach_form, true)
        on("click", ".delete-exercise", delete_power_exercise, true)

        show_toast("Exercise added successfully", "success")
    }

    ajax_post("/api/power-training-exercises/", formData, done_callback, FAIL_CALLBACK)
}

function delete_power_exercise(event) {
    event.preventDefault()
    let exercise = event.target.parentElement.parentElement.parentElement
    let exercise_container = exercise.parentElement

    let formData = {
        exercise: exercise.getAttribute("data-exercise-id"),
    }

    let done_callback = response => {
        exercise.remove();
        if (exercise_container.querySelectorAll("div").length === 0) {
            exercise_container.innerHTML = "<h6 class='card-title' id='no-exercises-message'>No exercises yet</h6>"
        }
        show_toast("Exercise successfully deleted", "success")
    }

    ajax_post(
        `/api/power-training-exercises/${formData.exercise}`,
        formData,
        done_callback,
        FAIL_CALLBACK,
        "DELETE"
    )
}

function delete_approach(event) {
    let li_item = event.target.parentElement.parentElement.parentElement;
    let ul_item = li_item.parentElement

    if (li_item.hasAttribute("data-approach-id")) {
        let formData = {
            approach: li_item.getAttribute("data-approach-id"),
            exercise: ul_item.parentElement.getAttribute("data-exercise-id"),
        }
        let done_callback = response => {
            li_item.remove();
            show_toast("Approach successfully added.", "success")
        }

        ajax_post(
            `/api/approaches/${formData.approach}`,
            null,
            done_callback,
            FAIL_CALLBACK,
            "DELETE"
        )
    } else
        li_item.remove()
}

function chane_password() {
    let formData = {
        old_password: document.getElementById("currentPassword").value,
        new_password1: document.getElementById("newPassword").value,
        new_password2: document.getElementById("renewPassword").value,
    };
    let done_callback = response => show_toast("Password change successfully", "success")

    ajax_post("/api/user/me/update_password", formData, done_callback, FAIL_CALLBACK, "PUT")
}

function update_user(){
    let sex_select = document.getElementById("sex")
    let formData = {
        email: document.getElementById("Email").value,
        username: document.getElementById("username").value,
        first_name: document.getElementById("first_name").value,
        last_name: document.getElementById("last_name").value,
        sex: sex_select.options[sex_select.selectedIndex].value,
        birth_date: document.getElementById("birth_date").value,
        weight: document.getElementById("weight").value,
        height: document.getElementById("height").value,
    };

    let done_callback =
            response => show_toast("User updated successfully.", "success");

    ajax_post("/api/user/me", formData, done_callback, FAIL_CALLBACK, "PUT")
}



function get_training_information(element) {
    let result = {}
    result.id =  element.getAttribute("data-training-id");
    result.type = element.getAttribute("data-training-type");
    return result
}

function create_dish_count_form(event) {
    let select_element = document.getElementById("select_dish");
    let list_group = document.getElementById("meal_list_group");

    let new_li_element = document.createElement("li");

    let noDishMessage = document.getElementById("no-dish-message")
    if (noDishMessage) {
        noDishMessage.remove()
    }

    new_li_element.setAttribute("data-dish-id", select_element.options[select_element.selectedIndex].value);
    new_li_element.classList.add("list-group-item");
    new_li_element.innerHTML = `<div class="d-flex">
                                  <div class="card-title-container gap-2 justify-content-between">
                                      <input type="text"
                                             class="form-control"
                                             value="${select_element.options[select_element.selectedIndex].text}" disabled>
                                      <span>Weight</span>
                                      <input type="number"
                                             class="form-control weightInput"
                                             name="weight"/>
                                      <button class="btn btn-primary create-or-update-dish-count">Save</button>
                                      <i class="bi bi-x-circle-fill deleteDishCount deleteIcon"></i>
                                  </div>
                                </div>`
    list_group.appendChild(new_li_element);
    new_li_element.querySelector(".create-or-update-dish-count").addEventListener("click", create_or_update_dish);
    new_li_element.querySelector(".deleteDishCount").addEventListener("click", delete_dish_count);

}

function create_or_update_dish(event) {
    let li_element = event.target.parentElement.parentElement.parentElement;
    let weight = this.parentElement.querySelector('input[name="weight"]').value;

    let formData = {
        dish: li_element.getAttribute("data-dish-id"),
        weight: weight,
        meal: document.getElementById("meal_id").getAttribute("value"),
    }

    if (li_element.hasAttribute("data-dish-count-id")) {
        let dish_count_id = li_element.getAttribute("data-dish-count-id");
        let done_callback = response => show_toast("Successfully updated dish", "success");

        ajax_post(
            `/api/dish-counts/${dish_count_id}/`,
            formData,
            done_callback,
            FAIL_CALLBACK,
            "PATCH"
        )
    } else {
        let done_callback = response => {
            li_element.setAttribute("data-dish-count-id", response["id"]);
            event.target.textContent = "Update"
            show_toast("Successfully added dish", "success")
        }

        ajax_post("/api/dish-counts/", formData, done_callback, FAIL_CALLBACK)
    }
}

function delete_dish_count(event) {
    let li_element = event.target.parentElement.parentElement.parentElement;
    let ul_element = li_element.parentElement

    if (li_element.hasAttribute("data-dish-count-id")) {
        let dish_count = li_element.getAttribute("data-dish-count-id")

        let done_callback = response => {
            li_element.remove()
            if (ul_element.querySelectorAll("li").length === 0) {
                ul_element.innerHTML = "<h6 class='card-title' id='no-dish-message'>No dishes yet</h6>"
            }
            show_toast("Successfully deleted dish", "success")
        }

        ajax_post(
            `/api/dish-counts/${dish_count}`,
            null,
            done_callback,
            FAIL_CALLBACK,
            "DELETE"
        )

    } else
        li_element.remove()

    if (ul_element.querySelectorAll("li").length === 0)
        ul_element.innerHTML = "<h6 class='card-title' id='no-dish-message'>No dishes yet</h6>"
}

function on_check_sort(event) {
    if (event.target.checked) {
        document.getElementById("date-search-form").submit()
    }
}

function delete_exercise(event) {
    event.preventDefault();
    let element = event.target.parentElement.parentElement.parentElement
    let container = element.parentElement

    let id = element.dataset.id

    let success_callback = response => {
        element.remove()
        if (container.querySelectorAll("div").length === 0) {
            container.innerHTML = "<h6 class='card-title'>No exercises yet</h6>"
        }
        show_toast("Successfully deleted exercise", "success")
    }

    ajax_post(
        `/api/exercises/${id}/`,
        null,
        success_callback,
        FAIL_CALLBACK,
        "DELETE"
    )
}

function delete_dish(event) {
    event.preventDefault()
    let dish_element = event.target.parentElement.parentElement.parentElement
    let container = dish_element.parentElement

    let id = dish_element.dataset.id

    let success_callback = response => {
        dish_element.remove()
        if (container.querySelectorAll("div").length === 0) {
            container.innerHTML = "<h6 class='card-title'>No dishes yet</h6>"
        }
        show_toast("Successfully deleted dish", "success")
    }

    ajax_post(
        `/api/dishes/${id}/`,
        null,
        success_callback,
        FAIL_CALLBACK,
        "DELETE"
    )
}

function delete_meal(event) {
    event.preventDefault()
    let meal_element = event.target.parentElement.parentElement.parentElement
    let container = meal_element.parentElement

    let id = meal_element.dataset.id

    let success_callback = response => {
        meal_element.remove()
        if (container.querySelectorAll("div").length === 0) {
            container.innerHTML = "<h6 class='card-title'>No meals yet</h6>"
        }
        show_toast("Successfully deleted meal")
    }

    ajax_post(
        `/api/meals/${id}/`,
        null,
        success_callback,
        FAIL_CALLBACK,
        "DELETE"
    )

}

function update_statistic_card(container_id, filter_name_id, new_period, new_data) {
    document.getElementById(container_id).innerHTML = new_data
    document.getElementById(filter_name_id).innerHTML = ` | ${new_period}`
}

function change_filter_training_ratio(event) {
    let period = event.target.textContent
    let data_string = `period=${period}`

    let success_callback = response => {
        set_echart_data("training-types-ratio", response['data'])
        document.getElementById("training-ratio-span").textContent = `| ${period}`
    }

    ajax_get("/api/user/get_training_type_ratio", data_string, success_callback, FAIL_CALLBACK)
}

function change_avg_calories_filter(event) {
    let period = event.target.textContent
    let data_string = `period=${period}`

    let success_callback = response => {
        update_statistic_card("calories-container", "avg-calories-filter-name", period, response["data"])
    }

    ajax_get("/api/user/get_avg_calories_info", data_string, success_callback, FAIL_CALLBACK)
}

function change_avg_protein_filter(event) {
    let period = event.target.textContent
    let data_string = `period=${period}`

    let success_callback = response => {
        update_statistic_card("protein-container", "avg-protein-filter-name", period, response["data"])
    }

    ajax_get("/api/user/get_avg_protein_info", data_string, success_callback, FAIL_CALLBACK)
}

function change_avg_carbohydrates_filter(event) {
    let period = event.target.textContent
    let data_string = `period=${period}`

    let success_callback = response => {
        update_statistic_card(
            "carbohydrates-container",
            "avg-carbohydrates-filter-name",
            period,
            response["data"])
    }

    ajax_get(
        "/api/user/get_avg_carbohydrates_info",
        data_string,
        success_callback,
        FAIL_CALLBACK
    )
}

function change_avg_fats_filter(event) {
    let period = event.target.textContent
    let data_string = `period=${period}`

    let success_callback = response => {
        update_statistic_card("fats-container", "avg-fats-filter-name", period, response["data"])
    }

    ajax_get("/api/user/get_avg_fats_info", data_string, success_callback, FAIL_CALLBACK)
}

function change_total_km_cycling_filter(event) {
    let period = event.target.textContent
    load_total_km_by_period_and_training_type(period, "cycling")
}

function change_total_km_swimming_filter(event) {
    let period = event.target.textContent
    load_total_km_by_period_and_training_type(period, "swimming")
}

function change_total_km_jogging_filter(event) {
    let period = event.target.textContent
    load_total_km_by_period_and_training_type(period, "jogging")
}

function change_total_km_walking_filter(event) {
    let period = event.target.textContent
    load_total_km_by_period_and_training_type(period, "walking")
}

function load_all_statistics_of_main_page() {
    if (!document.getElementById("training-types-ratio")) {
        return
    }

    let LOAD_PERIOD = "This Month"

    // Init and load trainings ratio chart
    ajax_get("/api/user/get_training_type_ratio", "period=today", init_trainings_type_ratio_echart_callback, FAIL_CALLBACK);
    load_PFC_ratio_data_by_period(LOAD_PERIOD, init_PFC_ratio_echart_callback)


    ajax_get("/api/user/get_avg_fats_info", `period=${LOAD_PERIOD}`, (response) => {
        update_statistic_card("fats-container", "avg-fats-filter-name", LOAD_PERIOD, response["data"])
    }, FAIL_CALLBACK);

    ajax_get("/api/user/get_avg_protein_info", `period=${LOAD_PERIOD}`, (response) => {
        update_statistic_card("protein-container", "avg-protein-filter-name", LOAD_PERIOD, response["data"])
    }, FAIL_CALLBACK)

    ajax_get("/api/user/get_avg_carbohydrates_info", `period=${LOAD_PERIOD}`, (response) => {
        update_statistic_card("carbohydrates-container", "avg-carbohydrates-filter-name", LOAD_PERIOD, response["data"])
    }, FAIL_CALLBACK)

    ajax_get("/api/user/get_avg_calories_info", `period=${LOAD_PERIOD}`, (response) => {
        update_statistic_card("calories-container", "avg-calories-filter-name", LOAD_PERIOD, response["data"])
    }, FAIL_CALLBACK)

    load_total_km_by_period_and_training_type(LOAD_PERIOD, "jogging")
    load_total_km_by_period_and_training_type(LOAD_PERIOD, "walking")
    load_total_km_by_period_and_training_type(LOAD_PERIOD, "swimming")
    load_total_km_by_period_and_training_type(LOAD_PERIOD, "cycling")

}

function change_pfc_ratio_filter(event) {
    let period = event.target.textContent
    let success_callback = response => {
        set_echart_data("PFC-ratio", response['data'])
        document.getElementById("PFC-span").textContent = `| ${period}`
    }
    load_PFC_ratio_data_by_period(period, success_callback)
}

function load_total_km_by_period_and_training_type(period, training_type) {
    let data_string = `period=${period}`
    let success_callback = response => {
        update_statistic_card(`${training_type}-km-container`, `total-km-${training_type}-filter-name`, period, response["data"])
    }

    ajax_get(`/api/user/get_total_km_by_${training_type}`, data_string, success_callback, FAIL_CALLBACK)
}

function load_PFC_ratio_data_by_period(period, success_callback) {
    let data_string = `period=${period}`
    ajax_get("/api/user/get_pfc_ratio", data_string, success_callback, FAIL_CALLBACK)
}