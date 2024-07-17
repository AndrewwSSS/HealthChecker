const SUCCESSES_ICON = '<i class="bi bi-check-circle-fill"></i>'
const ERROR_ICON = '<i class="bi bi-x-circle-fill"></i>'
const TOAST_SHOW_DURATION = 5000


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

function ajax_post(url, data, done_callback, fail_callback, dataType = "json") {
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        dataType: dataType,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
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

    let fail_callback = (XMLHttpRequest, textStatus, errorThrown) =>   {
        show_toast(`${errorThrown}`, "error")
    }

    ajax_post("/api/trainings/delete_training", formData, success_callback, fail_callback)
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
        formData.approach_id =li_item.getAttribute("data-approach-id")

        let done_callback = response => show_toast("Approach successfully added.", "success")
        let fail_callback = (XMLHttpRequest, textStatus, errorThrown) => show_toast(`${textStatus}. ${errorThrown}`, "error")

        ajax_post("/api/update_approach", formData, done_callback, fail_callback)
    } else {
        let done_callback = response => {
            event.target.textContent = "Update"
            li_item.setAttribute("data-approach-id", response["approach_id"]);
            show_toast("Approach successfully added.", "success")
        }
        let fail_callback = (XMLHttpRequest, textStatus, errorThrown) => show_toast(`${textStatus}. ${errorThrown}`, "error")
        ajax_post("/api/add_approach", formData, done_callback, fail_callback)
    }


}

function create_power_exercise() {
    let select_item = document.getElementById("select_exercise")

    let formData = {
        training_id: document.getElementById("training_id").getAttribute("value"),
        exercise_id: select_item.options[select_item.selectedIndex].value,
    }

    let done_callback = response => {
        let exercise_container = document.getElementById("exercise-container")
        let exercise_name = select_item.options[select_item.selectedIndex].text

        let noExerciseMessage = document.getElementById("no-exercises-message")
        if (noExerciseMessage)
            noExerciseMessage.remove()

        let div = document.createElement("div")
        div.setAttribute("data-exercise-id", `${response["power_training_id"]}`)
        div.innerHTML = (`<div class="card-title-container mb-3">
                              <span>${exercise_name}</span>
                              <div class="card-title-container gap-2">
                                  <button class="btn btn-primary addApproach">Add approach</button>
                                  <button class="btn btn-danger deleteExercise">Delete</button>
                              </div>
                          </div>
                          <ul class="list-group mb-3"></ul>`)
        exercise_container.appendChild(div)
        on("click", ".addApproach", create_approach_form, true)
        on("click", ".deleteExercise", delete_power_exercise, true)
        // card.querySelector(".deleteExercise").addEventListener('click', delete_exercise);
        // card.querySelector(".addApproach").addEventListener('click', add_approach_form);

        show_toast("Exercise added successfully", "success")
    }
    let fail_callback = (XMLHttpRequest, textStatus, errorThrown) => show_toast(`${textStatus}. ${errorThrown}`, "error")

    ajax_post("/api/add_power_training_exercise", formData, done_callback, fail_callback)
}

function delete_power_exercise(event) {
    event.preventDefault()
    let exercise = event.target.parentElement.parentElement.parentElement
    let exercise_container = exercise.parentElement

    let formData = {
        exercise_id: exercise.getAttribute("data-exercise-id"),
        training_id: document.getElementById("training_id").value,
    }

    let done_callback = response => {
        exercise.remove();
        if (exercise_container.querySelectorAll("div").length === 0) {
            exercise_container.innerHTML = "<h6 class='card-title' id='no-exercises-message'>No exercises yet</h6>"
        }
        show_toast("Exercise successfully deleted", "success")
    }
    let fail_callback =
        (jqXHR, textStatus, errorThrown) => show_toast(`${errorThrown}`, "error")

    ajax_post("/api/delete_power_exercise", formData, done_callback, fail_callback)
}

function delete_approach(event) {
    let li_item = event.target.parentElement.parentElement.parentElement;
    let ul_item = li_item.parentElement

    if (li_item.hasAttribute("data-approach-id")) {
        let formData = {
            approach_id: li_item.getAttribute("data-approach-id"),
            exercise_id: ul_item.parentElement.getAttribute("data-exercise-id"),
        }
        let done_callback = response => {
            li_item.remove();
            show_toast("Approach successfully added.", "success")
        }
        let fail_callback = (XMLHttpRequest, textStatus, errorThrown) => show_toast(`${textStatus}. ${errorThrown}`, "error")
        ajax_post("/api/delete_approach", formData, done_callback, fail_callback)
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

    let fail_callback = (XMLHttpRequest, textStatus, errorThrown) => show_toast(`${textStatus}. ${errorThrown}`, "error")
    ajax_post("/api/change_password", formData, done_callback, fail_callback)
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
    let fail_callback =
        (XMLHttpRequest, textStatus, errorThrown) => {
            console.log(errorThrown)
            show_toast(`${textStatus}. ${errorThrown}`, "error")
        }

    ajax_post("/api/user_update", formData, done_callback, fail_callback)
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
                                      <button class="btn btn-danger deleteDishCount">Delete</button>
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
        formData.dish_count = li_element.getAttribute("data-dish-count-id");
        let done_callback = response => show_toast("Successfully updated dish", "success");
        let fail_callback = (jqXHR, textStatus, errorThrown) => show_toast(`${textStatus}. ${errorThrown}`, "error");

        ajax_post("/api/update_dish_count", formData, done_callback, fail_callback)
    } else {
        let done_callback = response => {
            li_element.removeAttribute("data-dish-id")
            li_element.setAttribute("data-dish-count-id", response["dish_count_id"]);
            event.target.textContent = "Update"
            show_toast("Successfully added dish", "success")
        }
        let fail_callback =
            (jqXHR, textStatus, errorThrown) => show_toast(`${textStatus}. ${errorThrown}`, "error")

        ajax_post("/api/add_dish_to_meal", formData, done_callback, fail_callback)
    }
}

function delete_dish_count(event) {
    let li_element = event.target.parentElement.parentElement.parentElement;
    let ul_element = li_element.parentElement

    if (li_element.hasAttribute("data-dish-count-id")) {
        let formData = {
            dish_count: li_element.getAttribute("data-dish-count-id"),
        }

        let done_callback = response => {
            li_element.remove()
            if (ul_element.querySelectorAll("li").length === 0) {
                ul_element.innerHTML = "<h6 class='card-title' id='no-dish-message'>No dishes yet</h6>"
            }
            show_toast("Successfully deleted dish", "success")
        }
        let fail_callback =
            (jqXHR, textStatus, errorThrown) => show_toast(`${textStatus}. ${errorThrown}`, "error")

        ajax_post("/api/delete_dish_count", formData, done_callback, fail_callback)

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

    let formData = {
        exercise_id: element.dataset.id,
    }

    let success_callback = response => {
        element.remove()
        if (container.querySelectorAll("div").length === 0) {
            container.innerHTML = "<h6 class='card-title'>No exercises yet</h6>"
        }
        show_toast("Successfully deleted exercise", "success")
    }

    let fail_callback = (XMLHttpRequest, textStatus, errorThrown) => {
        show_toast(`${errorThrown}`, "error")
    }

    ajax_post("/api/delete_exercise", formData, success_callback, fail_callback)

}

function delete_dish(event) {
    event.preventDefault()
    let dish_element = event.target.parentElement.parentElement.parentElement
    let container = dish_element.parentElement

    let formData = {
        dish_id: dish_element.dataset.id,
    }

    let success_callback = response => {
        dish_element.remove()
        if (container.querySelectorAll("div").length === 0) {
            container.innerHTML = "<h6 class='card-title'>No dishes yet</h6>"
        }
        show_toast("Successfully deleted dish", "success")
    }

    let fail_callback = (XMLHttpRequest, textStatus, errorThrown) => {
        show_toast(`${errorThrown}`, "error")
    }

    ajax_post("/api/delete_dish", formData, success_callback, fail_callback)
}


function delete_meal(event) {
    event.preventDefault()
    let meal_element = event.target.parentElement.parentElement.parentElement
    let container = meal_element.parentElement

    let formData = {
        meal_id: meal_element.dataset.id
    }

    let success_callback = response => {
        meal_element.remove()
        if (container.querySelectorAll("div").length === 0) {
            container.innerHTML = "<h6 class='card-title'>No meals yet</h6>"
        }
        show_toast("Successfully deleted meal")
    }

    let fail_callback = (XMLHttpRequest, textStatus, errorThrown) => {
        show_toast(`${errorThrown}`, "error")
    }

    ajax_post("/api/delete_meal", formData, success_callback, fail_callback)

}


(function() {
    "use strict";

    on("click", ".deleteApproach", delete_approach, true);
    on("click", ".addApproach", create_approach_form, true)
    on("click", "#addExercise", create_power_exercise, true)
    on("click", ".deleteExercise", delete_power_exercise, true)
    on("click", "#change-password-btn", chane_password)
    on("click", "#changeUserBtn", update_user)
    on("click", "#addDish", create_dish_count_form)
    on("click", ".deleteDishCount", delete_dish_count, true)
    on("click", ".saveApproach", create_or_update_approach, true)
    on("click", ".create-or-update-dish-count", create_or_update_dish, true)
    on('click', '.toggle-sidebar-btn', function() {
        select('body').classList.toggle('toggle-sidebar')
    })
    on('click', '.form-check', on_check_sort, true)
    on('click', '.search-bar-toggle', function(e) {
        select('.search-bar').classList.toggle('search-bar-show')
    }, true)
    on("click", ".formSendButton", function(e) {
        e.target.classList.add('disabled')
        setTimeout(function () {
            e.target.classList.remove('disabled')
        }, TOAST_SHOW_DURATION)
    }, true)

    select(".delete-training-icon", true).forEach(element => {
        element.addEventListener('click', delete_training, false)
    })

    select(".delete-exercise-icon", true).forEach(element => {
        element.addEventListener('click', delete_exercise, false)
    })

    select(".delete-dish-icon", true).forEach(element => {
        element.addEventListener('click', delete_dish, false)
    })

    select(".delete-meal-icon", true).forEach(element => {
        element.addEventListener('click', delete_meal, false)
    })


    let navbarlinks = select('#navbar .scrollto', true)
    const navbarlinksActive = () => {
        let position = window.scrollY + 200
        navbarlinks.forEach(navbarlink => {
            if (!navbarlink.hash) return
            let section = select(navbarlink.hash)
            if (!section) return
            if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
                navbarlink.classList.add('active')
            } else {
                navbarlink.classList.remove('active')
            }
        })
    }
    window.addEventListener('load', navbarlinksActive)
    onscroll(document, navbarlinksActive)

    /**
     * Toggle .header-scrolled class to #header when page is scrolled
     */
    let selectHeader = select('#header')
    if (selectHeader) {
        const headerScrolled = () => {
            if (window.scrollY > 100) {
                selectHeader.classList.add('header-scrolled')
            } else {
                selectHeader.classList.remove('header-scrolled')
            }
        }
        window.addEventListener('load', headerScrolled)
        onscroll(document, headerScrolled)
    }

    /**
     * Back to top button
     */
    let backtotop = select('.back-to-top')
    if (backtotop) {
        const toggleBacktotop = () => {
            if (window.scrollY > 100) {
                backtotop.classList.add('active')
            } else {
                backtotop.classList.remove('active')
            }
        }
        window.addEventListener('load', toggleBacktotop)
        onscroll(document, toggleBacktotop)
    }

    /**
     * Initiate tooltips
     */
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })


    /**
     * Initiate TinyMCE Editor
     */

    const useDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isSmallScreen = window.matchMedia('(max-width: 1023.5px)').matches;

    // tinymce.init({
    //     selector: 'textarea.tinymce-editor',
    //     plugins: 'preview importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media codesample table charmap pagebreak nonbreaking anchor insertdatetime advlist lists wordcount help charmap quickbars emoticons accordion',
    //     editimage_cors_hosts: ['picsum.photos'],
    //     menubar: 'file edit view insert format tools table help',
    //     toolbar: "undo redo | accordion accordionremove | blocks fontfamily fontsize | bold italic underline strikethrough | align numlist bullist | link image | table media | lineheight outdent indent| forecolor backcolor removeformat | charmap emoticons | code fullscreen preview | save print | pagebreak anchor codesample | ltr rtl",
    //     autosave_ask_before_unload: true,
    //     autosave_interval: '30s',
    //     autosave_prefix: '{path}{query}-{id}-',
    //     autosave_restore_when_empty: false,
    //     autosave_retention: '2m',
    //     image_advtab: true,
    //     link_list: [{
    //         title: 'My page 1',
    //         value: 'https://www.tiny.cloud'
    //     },
    //         {
    //             title: 'My page 2',
    //             value: 'http://www.moxiecode.com'
    //         }
    //     ],
    //     image_list: [{
    //         title: 'My page 1',
    //         value: 'https://www.tiny.cloud'
    //     },
    //         {
    //             title: 'My page 2',
    //             value: 'http://www.moxiecode.com'
    //         }
    //     ],
    //     image_class_list: [{
    //         title: 'None',
    //         value: ''
    //     },
    //         {
    //             title: 'Some class',
    //             value: 'class-name'
    //         }
    //     ],
    //     importcss_append: true,
    //     file_picker_callback: (callback, value, meta) => {
    //         /* Provide file and text for the link dialog */
    //         if (meta.filetype === 'file') {
    //             callback('https://www.google.com/logos/google.jpg', {
    //                 text: 'My text'
    //             });
    //         }
    //
    //         /* Provide image and alt text for the image dialog */
    //         if (meta.filetype === 'image') {
    //             callback('https://www.google.com/logos/google.jpg', {
    //                 alt: 'My alt text'
    //             });
    //         }
    //
    //         /* Provide alternative source and posted for the media dialog */
    //         if (meta.filetype === 'media') {
    //             callback('movie.mp4', {
    //                 source2: 'alt.ogg',
    //                 poster: 'https://www.google.com/logos/google.jpg'
    //             });
    //         }
    //     },
    //     height: 600,
    //     image_caption: true,
    //     quickbars_selection_toolbar: 'bold italic | quicklink h2 h3 blockquote quickimage quicktable',
    //     noneditable_class: 'mceNonEditable',
    //     toolbar_mode: 'sliding',
    //     contextmenu: 'link image table',
    //     skin: useDarkMode ? 'oxide-dark' : 'oxide',
    //     content_css: useDarkMode ? 'dark' : 'default',
    //     content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }'
    // });

    /**
     * Initiate Bootstrap validation check
     */
    var needsValidation = document.querySelectorAll('.needs-validation')

    Array.prototype.slice.call(needsValidation)
        .forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })

    /**
     * Initiate Datatables
     */
    const datatables = select('.datatable', true)
    datatables.forEach(datatable => {
        new simpleDatatables.DataTable(datatable, {
            perPageSelect: [5, 10, 15, ["All", -1]],
            columns: [{
                select: 2,
                sortSequence: ["desc", "asc"]
            },
                {
                    select: 3,
                    sortSequence: ["desc"]
                },
                {
                    select: 4,
                    cellClass: "green",
                    headerClass: "red"
                }
            ]
        });
    })

    const mainContainer = select('#main');
    if (mainContainer) {
        setTimeout(() => {
            new ResizeObserver(function() {
                select('.echart', true).forEach(getEchart => {
                    echarts.getInstanceByDom(getEchart).resize();
                })
            }).observe(mainContainer);
        }, 100);
    }
})();


