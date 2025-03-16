// Copyright (C) 2025 DROMO SA

// This file is part of VOYA.
//
// VOYA is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// [Project Name] is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.


// Items functionalities
document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll("[id=section]");
    const servicesDataMap = {}; // Cache services data for each section dynamically

    // Utility Functions: Initialize Flatpickr
    const initializeFlatpickr = () => {
        const flatpickrFields = document.querySelectorAll(".flatpickr");
        flatpickrFields.forEach(field => {
            if (!field._flatpickr) {
                flatpickr(field, {dateFormat: "Y-m-d"});
            }
        });
    };

    // Fetching service based on the section name
    const fetchServices = (sectionName) => {
        if (servicesDataMap[sectionName]) return Promise.resolve(servicesDataMap[sectionName]); // Use cached data
        return fetch(`/proposals/api/services/${sectionName}/`)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return response.json();
            })
            .then(data => {
                servicesDataMap[sectionName] = data; // Cache data
                return data;
            })
            .catch(error => console.error(`Error fetching services for ${sectionName}:`, error));
    };

    // Logic to populate service dropdown with services based on the chosed city
    const populateServiceDropdown = (serviceDropdown, sectionName, city) => {
        fetchServices(sectionName).then(data => {
            city = parseInt(city, 10);
            const filteredServices = data.filter(service => parseInt(service.city_id, 10) === city);
            serviceDropdown.innerHTML = "<option value=''>Select a Service</option>";
            filteredServices.forEach(service => {
                const option = document.createElement("option");
                option.value = service.id;
                option.textContent = service.display_field;
                serviceDropdown.appendChild(option);
            });
        });
    };

    // Logic to clear row inputs (to be used when rows are added)
    const clearRowInputs = (row) => {
        const inputs = row.querySelectorAll("input, select, textarea");
        inputs.forEach(input => {
            if (input.tagName === "SELECT") {
                input.selectedIndex = 0;
                input.value = "";
            } else if (input.tagName === "TEXTAREA") {
                input.value = ""; // Clear textarea
            } else {
                input.value = "";
            }
            calculateBudget();
        });
    };

    // Logic to update items price and quantity fields after service field is populated
    const updatePriceQuantityField = (serviceDropdown, sectionName, priceField, quantityField) => {
        serviceDropdown.addEventListener("change", function () {
            const selectedServiceId = serviceDropdown.value;
            fetchServices(sectionName).then(data => {
                const selectedService = data.find(service => service.id == selectedServiceId);
                quantityField.value = "1";
                priceField.value = selectedService
                    ? `€ ${parseFloat(selectedService.price).toFixed(2)}`
                    : "";
                calculateBudget();
            });
        });
    };

    // Initialize Service Dropdowns
    sections.forEach(section => {
        const sectionName = section.textContent.trim();
        const tripSection = section.closest(".trip-section");
        const serviceDropdown = tripSection.querySelector("#service-dropdown");
        const cityDropdown = tripSection.querySelector("#city-dropdown");
        const servicePriceField = tripSection.querySelector("#service-price");
        const serviceQuantityField = tripSection.querySelector("input[name='quantity']");

        if (sectionName && serviceDropdown) {
            cityDropdown.addEventListener("change", function () {
                const selectedCity = cityDropdown.value;
                populateServiceDropdown(serviceDropdown, sectionName, selectedCity);
                servicePriceField.value = "€ 0.00";
                serviceQuantityField.value = "0";
            });

            updatePriceQuantityField(serviceDropdown, sectionName, servicePriceField, serviceQuantityField);
        }
    });

    // Add Row Functionality
    const addRowButtons = document.querySelectorAll(".add-option a");
    addRowButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const tripSection = button.closest(".trip-section");
            const section = tripSection.querySelector(".title").textContent.trim();
            const table = tripSection.querySelector(".requests-table");

            let lastRow
            let lastDescriptionRow
            let newDescriptionRow

            if (section === "Other Services" || section === "Other Services - Fixed" || section === "Other Services - Variable") {
                lastRow = table.querySelector(".table-row:last-of-type");
            } else {
                // Get all table rows and exclude headers
                let rows = [...table.querySelectorAll(".table-row")];

                // Ensure we get the last actual `.table-row` (the one before the last row)
                lastRow = rows.length > 1 ? rows[rows.length - 2] : rows[0];
                lastDescriptionRow = lastRow ? lastRow.nextElementSibling : null;


                if (!lastRow || !lastDescriptionRow.classList.contains("description-row")) {
                    console.error("Error:  Description row not found.");
                    return;
                }
            }

            const newRow = lastRow.cloneNode(true);
            if (lastDescriptionRow) {
                newDescriptionRow = lastDescriptionRow.cloneNode(true);
            }

            // Clears the new rows
            // clearRowInputs(newRow);


            // Copy all the input/select values from the last rows
            const lastRowInputs = lastRow.querySelectorAll("input, select");
            // const lastDescriptionRowInputs = lastDescriptionRow.querySelectorAll("input, select");
            const newRowInputs = newRow.querySelectorAll("input, select");
            // const newDescriptionRowInputs = newDescriptionRow.querySelectorAll("input, select");

            newRowInputs.forEach((newInput, index) => {
                const lastInput = lastRowInputs[index];

                if (lastInput) {
                    if (newInput.tagName === "SELECT") {
                        newInput.value = lastInput.value; // Copy selected option in the new row
                    } else {
                        if (newInput.id === "id_corresponding_trip_date") {
                            // Handel date field: set to the next day
                            if (lastInput.value) {
                                const lastDate = lastInput.value ? new Date(lastInput.value) : new Date();
                                lastDate.setDate(lastDate.getDate() + 1); // Add 1 day
                                newInput.value = lastDate.toISOString().split("T")[0]; //Set format to YYYY-MM-DD
                            }
                        } else {
                            newInput.value = lastInput.value; // Copy input values in the new row
                        }
                    }
                }
            });

            table.appendChild(newRow);
            if (newDescriptionRow) {
                table.appendChild(newDescriptionRow);
                initializeToggleDescription();
            }

            initializeDragAndDrop(table); //Re-enable drag-and-drop for new row
            updateRowOrder(); // Assign new order

            initializeFlatpickr(); // Ensure date picker works for new row
            // Populate city and service dropdown and update price and quantity
            const sectionName = tripSection.querySelector(".title").textContent.trim();
            const cityDropdown = newRow.querySelector("#city-dropdown");
            const serviceDropdown = newRow.querySelector("#service-dropdown");
            const servicePriceField = newRow.querySelector("#service-price");
            const serviceQuantityField = newRow.querySelector("input[name='quantity']");

            if (cityDropdown && serviceDropdown) {
                cityDropdown.addEventListener("change", function () {
                    const selectedCity = cityDropdown.value;
                    populateServiceDropdown(serviceDropdown, sectionName, selectedCity);
                    servicePriceField.value = "€ 0.00";
                    serviceQuantityField.value = "0";
                });

                updatePriceQuantityField(serviceDropdown, sectionName, servicePriceField, serviceQuantityField);
            }
        });
    });

    // Remove Row Functionality
    document.addEventListener("click", function (event) {
        if (event.target.closest(".remove-row-button")) {
            event.preventDefault();
            const row = event.target.closest(".table-row");
            const descriptionRow = row.nextElementSibling;
            const table = row.parentNode;

            // Count only main rows (exclude description rows)
            const mainRows = Array.from(table.children).filter(
                (r) => !r.classList.contains("description-row")
            );
            if (mainRows.length > 2) {
                row.remove();
                if (descriptionRow && descriptionRow.classList.contains("description-row")) {
                    descriptionRow.remove()
                }
            } else {
                if (row) {
                    clearRowInputs(row);
                }

                if (descriptionRow) {
                    clearRowInputs(descriptionRow);
                }
                initializeFlatpickr(); // Ensure date picker works for new row
                // Populate city and service dropdown and update price and quantity
                const tripSection = table.closest(".trip-section");
                const sectionName = tripSection.querySelector(".title").textContent.trim();
                const cityDropdown = row.querySelector("#city-dropdown");
                const serviceDropdown = row.querySelector("#service-dropdown");
                const servicePriceField = row.querySelector("#service-price");
                const serviceQuantityField = row.querySelector("input[name='quantity']");

                if (cityDropdown && serviceDropdown) {
                    cityDropdown.addEventListener("change", function () {
                        const selectedCity = cityDropdown.value;
                        populateServiceDropdown(serviceDropdown, sectionName, selectedCity);
                        servicePriceField.value = "€ 0.00";
                        serviceQuantityField.value = "0";
                    });

                    updatePriceQuantityField(serviceDropdown, sectionName, servicePriceField, serviceQuantityField);
                }

            }
        }
    });


    // Initialize Flatpickr on Page Load
    initializeFlatpickr();
});


// Toggle description initializer filed function
function initializeToggleDescription() {
    document.querySelectorAll(".toggle-description-btn").forEach(button => {
        button.removeEventListener("click", toggleDescription); //Prevent duplicate event listeners
        button.addEventListener("click", toggleDescription);
    });
}

// Toggle description filed function
function toggleDescription(event) {
    event.preventDefault();
    const button = event.currentTarget;
    const row = button.closest(".table-row");
    const descriptionRow = row.nextElementSibling; // Find the next row
    const img = button.querySelector("img");

    if (descriptionRow && descriptionRow.classList.contains("description-row")) {
        //Toggle visibility
        if (descriptionRow.style.display === "none" || descriptionRow.style.display === "") {
            descriptionRow.style.display = "block";
            img.src = img.getAttribute("data-open");
        } else {
            descriptionRow.style.display = "none";
            img.src = img.getAttribute("data-close");
        }

    }

}

document.addEventListener("DOMContentLoaded", function () {
    initializeToggleDescription();
});


function initializeDragAndDrop(table) {
    const rows = table.querySelectorAll(".table-row:not(.description-row)");

    rows.forEach((row) => {
        row.draggable = true;

        let draggedRow = null;
        let draggedDescriptionRow = null;

        row.addEventListener("dragstart", function (event) {
            draggedRow = this;
            draggedRow.classList.add("dragging");
            event.dataTransfer.setData("text/plain", null);

            // Find and track its associated description row
            draggedDescriptionRow = draggedRow.nextElementSibling;
            if (draggedDescriptionRow && draggedDescriptionRow.classList.contains("description-row")) {
                draggedDescriptionRow.classList.add("dragging");
            } else {
                draggedDescriptionRow = null;
            }

        });

        row.addEventListener("dragover", function (event) {
            event.preventDefault();
            const afterElement = getDragAfterElement(table, event.clientY);

            if (afterElement && afterElement !== draggedRow) {
                // Find the description row of the afterElement
                let targetDescriptionRow = afterElement.nextElementSibling;
                if (!targetDescriptionRow || !targetDescriptionRow.classList.contains("description-row")) {
                    targetDescriptionRow = null;
                }

                // **STEP 1: Move dragged row**
                if (draggedRow && afterElement) {
                    table.insertBefore(draggedRow, afterElement);
                }

                // **STEP 2: Move dragged description row (if exists)**
                if (draggedDescriptionRow && draggedDescriptionRow.classList.contains("description-row") && draggedRow.nextSibling) {
                    table.insertBefore(draggedDescriptionRow, draggedRow.nextSibling);
                }

                // **STEP 3: Move target's description row to maintain correct pair**
                if (targetDescriptionRow && targetDescriptionRow.classList.contains("description-row")) {
                    table.insertBefore(targetDescriptionRow, afterElement.nextSibling);
                }
            }
        });

        row.addEventListener("dragend", function () {
            draggedRow.classList.remove("dragging");

            // Also remove the "dragging" class from the description row

            if (draggedDescriptionRow && draggedDescriptionRow.classList.contains("description-row")) {
                draggedDescriptionRow.classList.remove("dragging");
            }

            fixMisplacedDescriptionRows(table);

            updateRowOrder();
        });

        row.addEventListener("drop", function (event) {
            event.preventDefault();
            if (draggedRow) {
                draggedRow.style.opacity = "1";
            }
            if (draggedDescriptionRow) {
                draggedDescriptionRow.style.opacity = "1";
            }

            fixMisplacedDescriptionRows(table);

            updateRowOrder();
        })
    });
}

function fixMisplacedDescriptionRows(table) {
    const rows = table.querySelectorAll(".table-row:not(.description-row)");

    rows.forEach(row => {
        const nextRow = row.nextElementSibling;
        if (!nextRow || !nextRow.classList.contains("description-row")) {
            const correctDescriptionRow = findMatchingDescriptionRow(row);
            if (correctDescriptionRow) {
                table.insertBefore(correctDescriptionRow, row.nextSibling);
            }
        }
    });

    // Ensure last row retains its description row
    const lastRow = table.querySelector(".table-row:last-of-type:not(.description-row)");
    if (lastRow) {
        const lastDescriptionRow = lastRow.nextElementSibling;
        if (!lastDescriptionRow || !lastDescriptionRow.classList.contains("description-row")) {
            const correctLastDescriptionRow = findMatchingDescriptionRow(lastRow);
            if (correctLastDescriptionRow) {
                table.appendChild(correctLastDescriptionRow);
            }
        }
    }
}

// Function to find the correct description row for a given row
function findMatchingDescriptionRow(row) {
    let nextRow = row.nextElementSibling;
    return nextRow && nextRow.classList.contains("description-row") ? nextRow : null;
}

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll(".table-row:not(.dragging)")];

    return draggableElements.reduce(
        (closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;

            if (offset < 0 && offset > closest.offset) {
                return {offset, element: child};
            } else {
                return closest;
            }
        },
        {offset: Number.NEGATIVE_INFINITY}
    ).element;
}

// Function to update row order
function updateRowOrder() {
    document.querySelectorAll("table-row:not(.description-row)").forEach((row, index) => {
        row.setAttribute("data-order", index + 1); // Assign the row dynamically
    });
}


// Row dragging functionality
document.addEventListener("DOMContentLoaded", function () {
    const tables = document.querySelectorAll(".requests-table");


    // Apply drag-and-drop to all existing tables on page load
    tables.forEach(table => initializeDragAndDrop(table));

    tables.forEach(table => {
        let draggedRow = null;

        // Enable dragging
        table.querySelectorAll(".table-row").forEach(row => {
            row.addEventListener("dragstart", function (event) {
                draggedRow = this;
                event.dataTransfer.effectAllowed = "move";
                setTimeout(() => (this.style.opacity = "0.5"), 0);
            });

            row.addEventListener("dragover", function (event) {
                event.preventDefault();
                event.dataTransfer.dropEffect = "move";

                const bounding = this.getBoundingClientRect();
                const offset = bounding.y + bounding.height / 2;

                if (event.clientY - offset > 0) {
                    this.parentNode.insertBefore(draggedRow, this.nextSibling);

                } else {
                    this.parentNode.insertBefore(draggedRow, this);
                }
            });

            row.addEventListener("dragend", function () {
                draggedRow.style.opacity = "1";
                updateRowOrder(table);
            });

            row.addEventListener("drop", function (event) {
                event.preventDefault();
                draggedRow.style.opacity = "1";
                updateRowOrder(table);
            });
        });
    });

    // Function to update row order
    // function updateRowIndexes(table) {
    //     table.querySelectorAll(".table-row").forEach((row, index) => {
    //         row.setAttribute("data-index", index + 1); // Assigning order dynamically
    //     });
    // }
});

// Functionality to submit proposal and budget forms and sends POST or PUT request to the API to save dynamic rows
document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.getElementById("submit-proposal-btn");
    const proposalForm = document.getElementById("proposal-form");

    if (!proposalForm) {
        console.error("Proposal form not found");
        return;
    }

    const mode = proposalForm.getAttribute("data-mode");
    const proposalId = proposalForm.getAttribute("data-proposal-id");
    const tripId = proposalForm.getAttribute("data-trip-id");

    submitButton.addEventListener("click", function () {
        console.log("Submit button clicked."); // Debugging


        // Getting the status of the proposal (Draft/In progress/Completed)
        const draftStatusElement = document.querySelector("#id_status");
        const draftStatus = draftStatusElement?.value; // Ensure it has a fallback value


        // let draftStatus
        // draftStatus = draftStatusField === "Draft" || draftStatusField === "In progress";


        // let draftStatusCheck = null;
        // if (draftStatus === "Not finished" || draftStatus === "In progress") {
        //     draftStatusCheck = true;
        // } else if (draftStatus === "Done") {
        //     draftStatusCheck = false;
        // }

        // Collect proposal data
        const proposalData = {
            title: document.querySelector("input[name='title']")?.value || "",
            status: draftStatus,
            internal_comments: document.querySelector(".internal-note textarea")?.value || "No notes",
        };

        console.log(`Proposal status is: ${draftStatus}`); // Debugging

        // Show Proposal validation errors if any
        if (!proposalData.title) {
            alert(`Proposal title is required. Please add a proposal title.`);
            return;
        } else if (!draftStatus) {
            alert(`Please set the current state of the proposal`);
            return;
        }

        // Validate rows for completeness and collection of items
        const itemsData = [];
        const invalidRows = [];

        // 1. Collect items data
        document.querySelectorAll(".table-row").forEach((row, index) => {
            const section_name = row.closest(".trip-section")?.querySelector(".title")?.textContent.trim() || ""; // Must match SectionChoices
            const serviceDropdown = row.querySelector("#service-dropdown");

            let service_id = null;
            if (section_name !== "Other Services - Fixed" && section_name !== "Other Services - Variable") {
                const selectedServices = serviceDropdown
                    ? Array.from(serviceDropdown.selectedOptions).map(option => parseInt(option.value, 10)).filter(Boolean)
                    : [];
                service_id = selectedServices[0]
            } else if (section_name === "Other Services - Fixed" && section_name !== "Other Services - Variable") {
                service_id = null;
            }

            const priceField = row.querySelector("#service-price")?.value.replace("€", "").trim();
            const cityField = row.querySelector("#city-dropdown") || row.querySelector(".col-2");

            let cityValue = cityField?.value && cityField.value !== "Select city" ? parseInt(cityField.value, 10) : null;

            const additionalNotesField = row.querySelector(".note textarea") || row.nextElementSibling?.querySelector(".description-field");
            const additionalNotes = additionalNotesField ? additionalNotesField.value.trim() : "No notes";

            // if (!cityValue || isNaN(cityValue)) {
            //     console.warn(`Invalid city value at row ${index + 1}:`, cityValue);
            // }

            // Initialize a data object to store row-specific values
            const rowData = {
                corresponding_trip_date: row.querySelector(".col-1 input")?.value || "", // YYYY-MM-DD format
                section_name: section_name,
                city: cityValue,
                quantity: parseInt(row.querySelector(".col-4 input")?.value || "0", 10), // Ensure integer
                price: parseFloat(priceField || "0.00"), // Handle autofill or placeholder
                service_id: service_id,
                additional_notes: additionalNotes,
                order: parseInt(row.getAttribute("data-order"), 10) || index + 1 // Track order dynamically
            };

            const hasData = Boolean(
                rowData.corresponding_trip_date ||
                rowData.city ||
                rowData.quantity > 0 ||
                rowData.price > 0 ||
                row.querySelector(".note textarea")?.value ||
                rowData.service_id
            );

            let isComplete
            if (section_name !== "Other Services - Fixed" && section_name !== "Other Services - Variable" && section_name !== "Other Services") {
                isComplete = Boolean(
                    rowData.corresponding_trip_date &&
                    rowData.city &&
                    rowData.service_id &&
                    rowData.quantity > 0 &&
                    rowData.price > 0
                );
            } else if (section_name === "Other Services - Fixed" || section_name === "Other Services - Variable") {
                isComplete = Boolean(
                    rowData.corresponding_trip_date &&
                    rowData.city &&
                    rowData.additional_notes &&
                    rowData.quantity > 0 &&
                    rowData.price > 0
                );
            }

            console.log(`Row ${rowData.order + 1} has data: ${hasData}, is complete: ${isComplete}`);
            console.log(`Has data: date - ${rowData.corresponding_trip_date}, 
                    city - ${rowData.city},
                    quantity - ${rowData.quantity},
                    price - ${rowData.price},
                    notes - ${row.querySelector(".note textarea")?.value},
                    service - ${rowData.service_id},`);

            // Only validate rows with data
            if (hasData && !isComplete) {
                invalidRows.push(rowData.section_name || `Row ${index + 1}`);
                row.classList.add("error-row");
            } else {
                row.classList.remove("error-row");
            }

            // Add valid rows to itemsData
            if (hasData && isComplete) {
                // rowData.additional_notes = row.querySelector(".note textarea")?.value || descriptionRow?.classList.contains("description-row")
                //     ? descriptionRow.querySelector(".description-field")?.value || "No notes" : "No notes";
                itemsData.push(rowData)
            }

        });
        // Show validation errors if any
        if (invalidRows.length > 0) {
            alert(`Please complete or clear the data rows in the following table(s): ${[...new Set(invalidRows)].join(", ")}`);
            return;
        }
        console.log("Final Items Data:", JSON.stringify(itemsData, null, 2));

        // Collect budget data
        const budgetData = [];
        const budgetTable = document.querySelector(".budget-table");
        const minPax = parseInt(budgetTable.querySelector("th:nth-child(2)").textContent.trim() || "0");
        const maxPax = parseInt(budgetTable.querySelector("th:nth-child(3)").textContent.trim() || "0");
        const focInput = budgetTable.querySelector("tbody tr:nth-child(3) th input")?.value || "0";
        const focAmountMinCell = budgetTable.querySelector("tbody tr:nth-child(3) td:nth-child(2)")?.textContent.trim().replace("€", "") || "0";
        const focAmountMaxCell = budgetTable.querySelector("tbody tr:nth-child(3) td:nth-child(3)")?.textContent.trim().replace("€", "") || "0";

        // Min Pax Budget
        budgetData.push({
            pax: minPax,
            variable_cost: parseFloat(budgetTable.querySelector("tbody tr:nth-child(1) td:nth-child(2)").textContent.replace("€", "").trim() || "0"),
            fixed_cost: parseFloat(budgetTable.querySelector("tbody tr:nth-child(2) td:nth-child(2)").textContent.replace("€", "")),
            free_of_charge: parseInt(focInput, 10), // Ensure integer conversion
            free_of_charge_amount: parseFloat(focAmountMinCell), // Correctly read and pass from the UI
            total_cost_per_person: parseFloat(budgetTable.querySelector("tbody tr:nth-child(4) td:nth-child(2)").textContent.replace("€", "").trim() || "0"),
            total_cost: parseFloat(budgetTable.querySelector("tbody tr:nth-child(5) td:nth-child(2)").textContent.replace("€", "").trim() || "0"),
            service_fee: parseFloat(budgetTable.querySelector("tbody tr:nth-child(6) td:nth-child(2) input").value.replace("€", "").trim() || "500.00"),
            margin: parseFloat(budgetTable.querySelector("tbody tr:nth-child(7) td:nth-child(2) input").value.replace("%", "").trim() || "10"),
            fina_price_per_person: parseFloat(budgetTable.querySelector("tfoot tr:nth-child(1) td:nth-child(2)").textContent.replace("€", "").trim() || "0"),
            final_price: parseFloat(budgetTable.querySelector("tfoot tr:nth-child(2) td:nth-child(2)").textContent.replace("€", "").trim() || "0"),
        });

        // Max Pax Budget
        budgetData.push({
            pax: maxPax,
            variable_cost: parseFloat(budgetTable.querySelector("tbody tr:nth-child(1) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
            fixed_cost: parseFloat(budgetTable.querySelector("tbody tr:nth-child(2) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
            free_of_charge: parseInt(focInput, 10),
            free_of_charge_amount: parseFloat(focAmountMinCell),
            total_cost_per_person: parseFloat(budgetTable.querySelector("tbody tr:nth-child(4) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
            total_cost: parseFloat(budgetTable.querySelector("tbody tr:nth-child(5) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
            service_fee: parseFloat(budgetTable.querySelector("tbody tr:nth-child(6) td:nth-child(3) input").value.replace("€", "").trim() || "500.00"),
            margin: parseFloat(budgetTable.querySelector("tbody tr:nth-child(7) td:nth-child(3) input").value.replace("%", "").trim() || "10"),
            fina_price_per_person: parseFloat(budgetTable.querySelector("tfoot tr:nth-child(1) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
            final_price: parseFloat(budgetTable.querySelector("tfoot tr:nth-child(2) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
        });

        // Determine API endpoint and method dynamically
        let apiURL, apiMethod
        if (mode === "create") {
            apiURL = `/proposals/api/create/${tripId}/`;
            apiMethod = "POST";
        } else if (mode === "edit" && proposalId) {
            apiURL = `/proposals/api/edit/${proposalId}/`;
            apiMethod = "PUT";
        } else {
            console.error("Invalid page mode or missing proposal ID.");
            alert("Something went wrong. Please refresh and try again.");
            return;
        }

        // Combine data and send to API
        const payload = {
            trip_id: tripId,
            proposal: proposalData,
            items: itemsData,
            budget: budgetData
        };
        console.log("Payload sent to API:", JSON.stringify(payload, null, 2));

        // const pk = "{{ proposal.id }}"
        fetch(apiURL, {
            method: apiMethod,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
            body: JSON.stringify(payload),
        })
            .then(async (response) => {
                if (!response.ok) {
                    const errorData = await response.json();  // Read error response
                    console.error("Full API Error Response:", errorData);
                    throw new Error(errorData.error || "Invalid item data");
                }
                return response.json();
            })
            .then((data) => {
                if (data.success) {
                    alert("Proposal saved successfully!");
                    window.location.href = `/proposals/${data.proposal_id || proposalId}/details/`;
                } else {
                    throw new Error(data.error || "Failed to save proposal.");
                }
            })
            .catch((error) => {
                console.error("Error saving proposal:", error);
                alert(`An error occurred: ${error.message}`);
                if (error.error) {
                    alert(`Error: ${error.error}\nDetails: ${JSON.stringify(error.details, null, 2)}`);
                } else {
                    alert("An unexpected error occurred. Please try again.");
                }

            });
    });
});

// Functionality to calculate the budget table
const calculateBudget = () => {
    const budgetTable = document.querySelector(".budget-table");
    const proposalTables = document.querySelectorAll(".requests-table");

    let variableCost = 0;
    let fixedCost = 0;

    // Calculate costs from the proposal tables
    proposalTables.forEach(table => {
        const rows = table.querySelectorAll(".table-row");

        rows.forEach(row => {
            const priceField = row.querySelector("#service-price");
            const quantityField = row.querySelector("input[name='quantity']");
            const price = parseFloat(priceField?.value.replace("€", "").trim()) || 0;
            const quantity = parseInt(quantityField?.value) || 0;

            // Classify costs based on section title
            const sectionTitle = table.closest(".trip-section").querySelector(".title").textContent || "";
            if (["Local Guides", "Tour Leader", "Transfers", "Private Transport", "Other Services - Fixed"].some(type => sectionTitle.includes(type))) {
                fixedCost += price * quantity;
            } else {
                variableCost += price * quantity;
            }
        });
    });

    // Update the budget table based on column headers
    const budgetHeaders = budgetTable.querySelectorAll("thead th");
    const budgetRows = budgetTable.querySelectorAll("tbody tr");
    const budgetFooterRows = budgetTable.querySelectorAll("tfoot tr")

    budgetHeaders.forEach((header, columnIndex) => {
        if (columnIndex === 0) {
            return
        }

        const headerText = header.textContent.trim();
        let paxMultiplier = 1; // Default multiplier for "Totals"

        if (headerText.includes("pax")) {
            paxMultiplier = parseInt(headerText.replace("pax", "").trim()) || 1;
        }

        // Safely update corresponding rows
        const variableCostCell = budgetRows[0]?.querySelectorAll("td")[columnIndex - 1];
        const fixedCostCell = budgetRows[1]?.querySelectorAll("td")[columnIndex - 1];
        const focCell = budgetRows[2]?.querySelector("th input");
        const focAmountCell = budgetRows[2]?.querySelectorAll("td")[columnIndex - 1];
        const totalCostPerPersonCell = budgetRows[3]?.querySelectorAll("td")[columnIndex - 1];
        const totalCostCell = budgetRows[4]?.querySelectorAll("td")[columnIndex - 1];
        const serviceFeeCell = budgetRows[5]?.querySelectorAll("td")[columnIndex - 1];
        const marginCell = budgetRows[6]?.querySelectorAll("td")[columnIndex - 1];
        const finalPricePerPersonCell = budgetFooterRows[0]?.querySelectorAll("td")[columnIndex - 1];
        const finalPriceCell = budgetFooterRows[1]?.querySelectorAll("td")[columnIndex - 1];

        // Extract text content safely
        const foc = parseFloat(focCell?.value || "0");
        const serviceFee = parseFloat(serviceFeeCell?.querySelector("input")?.value || "500");
        const margin = parseFloat(marginCell?.querySelector("input")?.value || "10");
        const focAmount = variableCost * foc;
        const totalPerPerson = variableCost + (focAmount / paxMultiplier) + (fixedCost / paxMultiplier);
        const totalCost = (variableCost * paxMultiplier) + focAmount + fixedCost

        if (variableCostCell) variableCostCell.textContent = `€ ${(variableCost).toFixed(2)}`;
        if (fixedCostCell) fixedCostCell.textContent = `€ ${(fixedCost).toFixed(2)}`;
        if (focAmountCell) focAmountCell.textContent = `€ ${(focAmount).toFixed(2)}`;
        if (totalCostPerPersonCell) totalCostPerPersonCell.textContent = `€ ${(totalPerPerson).toFixed(2)}`;
        if (totalCostCell) totalCostCell.textContent = `€ ${(totalCost).toFixed(2)}`;

        if (finalPricePerPersonCell) {
            const finalPricePerPerson = (totalPerPerson + (serviceFee / paxMultiplier)) * (1 + (margin / 100));
            finalPricePerPersonCell.textContent = `€ ${finalPricePerPerson.toFixed(2)}`;
        }
        if (finalPriceCell) {
            const finalPrice = (totalCost + serviceFee) * (1 + (margin / 100));
            finalPriceCell.textContent = `€ ${finalPrice.toFixed(2)}`;
        }

    });
};

//Budget Tabel Actions
document.addEventListener("DOMContentLoaded", function () {
    const budgetTable = document.querySelector(".budget-table");
    const proposalTables = document.querySelectorAll(".requests-table");

    // calculateBudget();


    // Utility Functions


    // Add listeners to "Service Fee" Free of charge ("FOC") and "Margin" inputs
    const serviceFeeInputs = budgetTable.querySelectorAll(
        "tbody tr:nth-child(6) td input"
    );
    const marginInputs = budgetTable.querySelectorAll(
        "tbody tr:nth-child(7) td input"
    );

    const focInput = budgetTable.querySelectorAll(
        "tbody tr:nth-child(3) th input"
    );

    if (serviceFeeInputs.length > 0) {
        serviceFeeInputs.forEach((input) => {
            input.addEventListener("input", calculateBudget);
        });
    }

    if (marginInputs.length > 0) {
        marginInputs.forEach((input) => {
            input.addEventListener("input", calculateBudget);
        });
    }

    if (focInput.length > 0) {
        focInput.forEach((input) => {
            input.addEventListener("input", calculateBudget);
        });
    }

    // Initial calculation on page load
    calculateBudget();


    // Set up a MutationObserver to watch for changes in the DOM
    proposalTables.forEach(table => {
        const observer = new MutationObserver(() => calculateBudget());

        // Watch for additions or removals of child nodes
        observer.observe(table, {childList: true});

        // Add listeners for changes in input fields
        table.addEventListener("input", (event) => {
            if (event.target.matches("#service-price, input[name='quantity'], select[id='service-dropdown']")) {
                calculateBudget();
            }
        });
    });

    // Initial calculation on page load
    calculateBudget();
});
