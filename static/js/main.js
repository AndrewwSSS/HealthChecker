(function() {
    "use strict";

    on("click", ".deleteApproach", delete_approach, true);
    on("click", ".addApproach", create_approach_form, true)
    on("click", "#addExercise", create_power_exercise, true)
    on("click", ".delete-exercise", delete_power_exercise, true)
    on("click", "#change-password-btn", chane_password)
    on("click", "#changeUserBtn", update_user)
    on("click", "#addDish", create_dish_count_form)
    on("click", ".deleteDishCount", delete_dish_count, true)
    on("click", ".saveApproach", create_or_update_approach, true)
    on("click", ".create-or-update-dish-count", create_or_update_dish, true)

    on("click", ".training-ratio-filter", change_filter_training_ratio, true)
    on("click", ".PFC-ratio-filter", change_pfc_ratio_filter, true)

    on("click", ".avg-calories-filter", change_avg_calories_filter, true)
    on("click", ".avg-protein-filter", change_avg_protein_filter, true)
    on("click", ".avg-carbohydrates-filter", change_avg_carbohydrates_filter, true)
    on("click", ".avg-fats-filter", change_avg_fats_filter, true)

    on("click", ".total-km-cycling-filter", change_total_km_cycling_filter, true)
    on("click", ".total-km-walking-filter", change_total_km_walking_filter, true)
    on("click", ".total-km-jogging-filter", change_total_km_jogging_filter, true)
    on("click", ".total-km-swimming-filter", change_total_km_swimming_filter, true)


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

    load_all_statistics_of_main_page()

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


