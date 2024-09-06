function update_meal_detail_info(response) {
    document.getElementById("total_calories").value = response["calories"];
    document.getElementById("total_fats").value = response["fats"];
    document.getElementById("total_protein").value = response["protein"];
    document.getElementById("total_carbohydrates").value = response["carbohydrates"];
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
        let done_callback = response => {
            update_meal_detail_info(response)
            show_toast("Successfully updated dish", "success");
        }

        ajax_post(
            `/api/dish-counts/${dish_count_id}/`,
            formData,
            done_callback,
            FAIL_CALLBACK,
            "PATCH"
        )
    } else {
        let done_callback = response => {
            update_meal_detail_info(response)
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
            update_meal_detail_info(response)
            li_element.remove()
            if (ul_element.querySelectorAll("li").length === 0) {
                ul_element.innerHTML = "<h6 class='card-title' id='no-dish-message'>No dishes yet</h6>"
            }
        }

        ajax_post(
            `/api/dish-counts/${dish_count}/`,
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
