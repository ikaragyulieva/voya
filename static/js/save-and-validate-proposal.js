// Copyright (C) 2025 DROMO SA

// This file is part of VOYA.
//
// VOYA is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Voya is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.

// Normalize section names across languages using Django context variables


function getProposalPayload() {
    const proposalForm = document.getElementById("proposal-form");

    if (!proposalForm) {
        console.error("Proposal form not found");
        return;
    }

    const mode = proposalForm.getAttribute("data-mode");
    const proposalId = proposalForm.getAttribute("data-proposal-id");
    const tripId = proposalForm.getAttribute("data-trip-id");

    const draftStatusElement = document.querySelector("#id_status");
    const draftStatus = draftStatusElement?.value; // Ensure it has a fallback value

    // Collect proposal data
    const proposalData = {
        id: parseInt(proposalId),
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
            const rawSectionName = row.closest(".trip-section")?.querySelector(".title") || ""; // Must match SectionChoices
            const section_name = getSectionKey(rawSectionName);
            const serviceDropdown = row.querySelector("#service-dropdown");

            let service_id = null;
            if (section_name !== "Other Services - Fixed" && section_name !== "Other Services - Variable" && section_name !== "Meals") {
                const selectedServices = serviceDropdown
                    ? Array.from(serviceDropdown.selectedOptions).map(option => parseInt(option.value, 10)).filter(Boolean)
                    : [];
                service_id = selectedServices[0]
            } else if (section_name === "Other Services - Fixed" && section_name !== "Other Services - Variable" && section_name !== "Meals") {
                service_id = null;
            }

            const priceField = row.querySelector("#service-price")?.value.replace("€", "").trim();
            const cityField = row.querySelector("#city-dropdown") || row.querySelector(".col-2");

            let cityValue = cityField?.value && cityField.value !== "Select city" ? parseInt(cityField.value, 10) : null;

            const additionalNotesField =
                row.querySelector(".note textarea") ||
                row.nextElementSibling?.querySelector(".description-field") ||
                row.querySelector("#meal-dropdown");
            const additionalNotes = additionalNotesField?.value?.trim() || "No notes";

            const itemId = row.getAttribute("data-id");
            const orderAttr = row.getAttribute("data-order");
            // Initialize a data object to store row-specific values
            const rowData = {
                corresponding_trip_date: row.querySelector(".col-1 input")?.value || "", // YYYY-MM-DD format
                section_name: section_name,
                city: cityValue,
                quantity: parseInt(row.querySelector(".col-4 input")?.value || "0", 10), // Ensure integer
                price: parseFloat(priceField || "0.00"), // Handle autofill or placeholder
                service_id: service_id,
                additional_notes: additionalNotes,
                order: orderAttr !== null ? parseInt(orderAttr, 10) : index + 1 // Track order dynamically
            };
            if (itemId) {
                rowData.id=parseInt(itemId);
            }

            const hasData = Boolean(
                rowData.corresponding_trip_date ||
                rowData.city ||
                rowData.quantity > 0 ||
                rowData.price > 0 ||
                row.querySelector(".note textarea")?.value ||
                rowData.service_id
            );

            let isComplete
            const isMealOrOtherService =
                section_name === "Other Services - Fixed" ||
                section_name === "Other Services - Variable" ||
                section_name === "Other Services" ||
                section_name === "Meals"

            if (!isMealOrOtherService) {
                isComplete = Boolean(
                    rowData.corresponding_trip_date &&
                    rowData.city &&
                    rowData.service_id &&
                    rowData.quantity > 0 &&
                    rowData.price > 0
                );
            } else if (isMealOrOtherService) {
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
        const minBudgetId = parseInt(budgetTable.querySelector("th:nth-child(2)").getAttribute("data-id"));
        const maxBudgetId = parseInt(budgetTable.querySelector("th:nth-child(3)").getAttribute("data-id"));
        // Min Pax Budget
        budgetData.push({
            pax: minPax,
            id: minBudgetId,
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
            id: maxBudgetId,
            variable_cost: parseFloat(budgetTable.querySelector("tbody tr:nth-child(1) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
            fixed_cost: parseFloat(budgetTable.querySelector("tbody tr:nth-child(2) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
            free_of_charge: parseInt(focInput, 10),
            free_of_charge_amount: parseFloat(focAmountMaxCell),
            total_cost_per_person: parseFloat(budgetTable.querySelector("tbody tr:nth-child(4) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
            total_cost: parseFloat(budgetTable.querySelector("tbody tr:nth-child(5) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
            service_fee: parseFloat(budgetTable.querySelector("tbody tr:nth-child(6) td:nth-child(3) input").value.replace("€", "").trim() || "500.00"),
            margin: parseFloat(budgetTable.querySelector("tbody tr:nth-child(7) td:nth-child(3) input").value.replace("%", "").trim() || "10"),
            fina_price_per_person: parseFloat(budgetTable.querySelector("tfoot tr:nth-child(1) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
            final_price: parseFloat(budgetTable.querySelector("tfoot tr:nth-child(2) td:nth-child(3)").textContent.replace("€", "").trim() || "0"),
        });

         // Combine data and send to API
        const payload = {
            trip_id: tripId,
            proposal: proposalData,
            items: itemsData,
            budget: budgetData,
            mode: mode,
        };
        console.log("Payload sent to API:", JSON.stringify(payload, null, 2));

        return payload;
}

document.getElementById("save-and-check-btn").addEventListener("click", function () {
    const payload = getProposalPayload();

    fetch(`/api/proposals/save-and-validate/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: JSON.stringify(payload),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                const results = data.validation_summary;
                let summary = `<h4>Validation Summary</h4>`;
                summary += `<p>Warnings: ${results.warnings}, Errors: ${results.errors}</p><ul>`;
                results.details.forEach(r => {
                    summary += `<li><strong>${r.check}</strong>: ${r.message}</li>`;
                });
                summary += "</ul>";
                showPopup(summary);
            } else {
                throw new Error(data.error || "Failed to save and validate.");
            }
        })
        .catch(error => {
            alert("An error occurred while saving and validating.")
            console.error(error);
        });
});
