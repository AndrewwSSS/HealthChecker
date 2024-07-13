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

function delete_training(type, id, success_callback, fail_callback) {
    let formData = {
        type: type,
        training_id: id,
    }
    $.ajax({
        type: "POST",
        url: "/api/trainings/delete_training",
        data: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        dataType: "json",
    }).done(success_callback).fail(fail_callback)
}
function add_approach_form(event) {
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
        power_training_exercise_id: li_item.parentElement.parentElement.getAttribute("data-exercise-id"),
    }
    if (li_item.hasAttribute("data-approach-id")) {
        formData.approach_id =li_item.getAttribute("data-approach-id")
        $.ajax({
            type: "POST",
            url: "/api/update_approach",
            data: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken")
            },
            dataType: "json",
        }).done(function (response) {
            show_toast("Approach successfully added.", "success")
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            show_toast(`${textStatus}. ${errorThrown}`, "error")
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/api/add_approach",
            data: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken")
            },
            dataType: "json",
        }).done(function (response) {
            event.target.textContent = "Update"
            li_item.setAttribute("data-approach-id", response["approach_id"]);
            show_toast("Approach successfully added.", "success")
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            show_toast(`${textStatus}. ${errorThrown}`, "error")
        })
    }


}


function add_exercise() {
    let select_item = document.getElementById("select_exercise")

    let formData = {
        training_id: $("#training_id").val(),
        exercise_id: select_item.options[select_item.selectedIndex].value,
    }

    $.ajax({
        type: "POST",
        url: "/api/add_power_training_exercise",
        data: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        dataType: "json",
    }).done(function (response) {
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
        on("click", ".addApproach", add_approach_form, true)
        on("click", ".deleteExercise", delete_exercise, true)
        // card.querySelector(".deleteExercise").addEventListener('click', delete_exercise);
        // card.querySelector(".addApproach").addEventListener('click', add_approach_form);

        show_toast("Exercise added successfully", "success")
    }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
        show_toast(`${textStatus}. ${errorThrown}`, "error")
    })
}

function delete_exercise(event) {
    let exercise = event.target.parentElement.parentElement.parentElement
    let exercise_container = exercise.parentElement

    let formData = {
        exercise_id: exercise.getAttribute("data-exercise-id"),
        training_id: document.getElementById("training_id").value,
    }
    $.ajax({
        type: "POST",
        url: "/api/delete_exercise",
        data: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        dataType: "json",
    }).done(function (data) {
        if (exercise_container.querySelectorAll("div").length === 0) {
            exercise_container.innerHTML = "<h6 class='card-title' id='no-exercises-message'>No exercises yet</h6>"
        }
        exercise.remove();
        show_toast("Exercise successfully deleted", "success")
    }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
        show_toast(`${textStatus}. ${errorThrown}`, "error")
    })
}

function delete_approach(event) {
    let li_item = event.target.parentElement.parentElement.parentElement;
    let ul_item = li_item.parentElement

    if (li_item.hasAttribute("data-approach-id")) {
        let formData = {
            approach_id: li_item.getAttribute("data-approach-id"),
            exercise_id: ul_item.parentElement.getAttribute("data-exercise-id"),
        }
        $.ajax({
            type: "POST",
            url: "/api/delete_approach",
            data: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken")
            },
            dataType: "json",
        }).done(function (response) {
            li_item.remove();
            // if (ul_item.querySelectorAll("li").length === 0) {
            //     ul_item.innerHTML = "<h6 class='card-title' id='no-exercises-message'>No exercises yet</h6>"
            // }
            show_toast("Approach successfully added.", "success")
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            show_toast(`${textStatus}. ${errorThrown}`, "error")
        })
    } else {
        li_item.remove()
    }

    // if (ul_item.querySelectorAll("li").length === 0) {
    //     ul_item.innerHTML = "<h6 class='card-title' id='no-exercises-message'>No exercises yet</h6>"
    // }
}

function chane_password(){
    let formData = {
        old_password: $("#currentPassword").val(),
        new_password1: $("#newPassword").val(),
        new_password2: $("#renewPassword").val(),
    };

    $.ajax({
        type: "POST",
        url: "/api/change_password",
        data: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        dataType: "json",
    }).done(function (data) {
        console.log(data);
        if (data.status === "error") {
            show_toast("Error. Invalid input", "error")
        }
        else if (data.status === "success") {
            show_toast("Password change successfully", "success")
        }

    }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
        show_toast(`${textStatus}. ${errorThrown}`, "error")
    })
}

function update_user(){
    let formData = {
        email: $("#Email").val(),
        username: $("#username").val(),
        first_name: $("#first_name").val(),
        last_name: $("#last_name").val(),

    };

    $.ajax({
        type: "POST",
        url: "/api/user_update",
        data: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
        },
        dataType: "json",
    }).done(function (data) {
        if(data.status === "success"){
            show_toast("User updated successfully.", "success");
        } else if(data.status === "error") {
            show_toast("User update error. Invalid input", "error");
        }
    })
}

function show_toast(msg, type) {
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

function delete_cycling_training(event) {
    let elem = event.target.parentElement.parentElement;
    let id = elem.getAttribute("data-training-id");

    delete_training("CY", id,
function (data) {
        elem.remove()
        show_toast("Successfully deleted training", "success")
    },
    function (XMLHttpRequest, textStatus, errorThrown) {
        show_toast(`${textStatus}. ${errorThrown}`, "error")
    });
}

function delete_power_training(event) {
    let elem = event.target.parentElement.parentElement;
    let id = elem.getAttribute("data-training-id");

    delete_training("PW", id,
        function (data) {
            elem.remove()
            show_toast("Successfully deleted training", "success")
        },
        function (XMLHttpRequest, textStatus, errorThrown) {
            show_toast(`${textStatus}. ${errorThrown}`, "error")
           }
    );
}

function add_dish_form(event) {
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
                                      <button class="btn btn-primary saveMealDish">Save</button>
                                      <button class="btn btn-danger deleteDishCount">Delete</button>
                                  </div>
                                </div>`
    list_group.appendChild(new_li_element);
    new_li_element.querySelector(".saveMealDish").addEventListener("click", save_dish);
    new_li_element.querySelector(".deleteDishCount").addEventListener("click", delete_dish);

}

function save_dish(event) {
    let li_element = event.target.parentElement.parentElement.parentElement;
    let dish_id = li_element.getAttribute("data-dish-id");
    let weight = this.parentElement.querySelector('input[name="weight"]').value;

    let formData = {
        dish_id: dish_id,
        weight: weight,
        meal_id: document.getElementById("meal_id").value,
    }

    if (li_element.hasAttribute("data-dish-count-id")) {
        formData.dish_count_id = li_element.getAttribute("data-dish-count-id");
        $.ajax({  type: "POST",
            url: "/api/update_dish_count",
            data: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken")
            },
            dataType: "json",
        }).done(function (response) {
            show_toast("Successfully updated dish", "success")
        }).fail(function (jqXHR, textStatus, errorThrown) {
            show_toast(`${textStatus}. ${errorThrown}`, "error")
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/api/add_dish_to_meal",
            data: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken")
            },
            dataType: "json",
        }).done(function (response) {
            li_element.removeAttribute("data-dish-id")
            li_element.setAttribute("data-dish-count-id", response["dish_count_id"]);
            event.target.textContent = "Update"
            show_toast("Successfully added dish", "success")
        }).fail(function (jqXHR, textStatus, errorThrown) {
            show_toast(`${textStatus}. ${errorThrown}`, "error")
        })
    }
}


function delete_dish(event) {
    let li_element = event.target.parentElement.parentElement.parentElement;
    let ul_element = li_element.parentElement

    if (li_element.hasAttribute("data-dish-count-id")) {
        let formData = {
            dish_count_id: li_element.getAttribute("data-dish-count-id"),
            meal_id: document.getElementById("meal_id").value,
        }
        $.ajax({
            type: "POST",
            url: "/api/delete_dish_count",
            data: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken")
            },
            dataType: "json",
        }).done(function (response) {
            li_element.remove()
            if (ul_element.querySelectorAll("li").length === 0) {
                ul_element.innerHTML = "<h6 class='card-title' id='no-dish-message'>No dishes yet</h6>"
            }
            show_toast("Successfully deleted dish", "success")
        }).fail(function (jqXHR, textStatus, errorThrown) {
            show_toast(`${textStatus}. ${errorThrown}`, "error")
        })
    } else {
        li_element.remove()
    }
    if (ul_element.querySelectorAll("li").length === 0) {
        ul_element.innerHTML = "<h6 class='card-title' id='no-dish-message'>No dishes yet</h6>"
    }
}

(function() {
    "use strict";

    on("click", ".deleteApproach", delete_approach, true);
    on("click", ".addApproach", add_approach_form, true)
    on("click", "#addExercise", add_exercise, true)
    on("click", ".deleteExercise", delete_exercise, true)
    on("click", ".deleteCyclingTraining", delete_cycling_training, true)
    on("click", ".deletePowerTraining", delete_power_training, true)
    on("click", "#change-password-btn", chane_password)
    on("click", "#changeUserBtn", update_user)
    on("click", "#addDish", add_dish_form)
    on("click", ".deleteDishCount", delete_dish, true)
    on("click", ".saveApproach", create_or_update_approach, true)
    on('click', '.toggle-sidebar-btn', function() {
        select('body').classList.toggle('toggle-sidebar')
    })
    on('click', '.search-bar-toggle', function(e) {
        select('.search-bar').classList.toggle('search-bar-show')
    }, true)


    on("click", ".formSendButton", function(e) {
        e.target.classList.add('disabled')
        setTimeout(function () {
            e.target.classList.remove('disabled')
        }, TOAST_SHOW_DURATION)
    }, true)


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


