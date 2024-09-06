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