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
        update_statistic_card(
            `${training_type}-km-container`, `total-km-${training_type}-filter-name`, period, response["data"]
        )
    }

    ajax_get(`/api/user/get_total_km_by_${training_type}`, data_string, success_callback, FAIL_CALLBACK)
}

function load_PFC_ratio_data_by_period(period, success_callback) {
    let data_string = `period=${period}`
    ajax_get("/api/user/get_pfc_ratio", data_string, success_callback, FAIL_CALLBACK)
}