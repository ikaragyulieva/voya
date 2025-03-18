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

