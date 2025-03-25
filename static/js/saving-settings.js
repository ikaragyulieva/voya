// Copyright (C) 2025 DROMO SA

// This file is part of VOYA.
//
// VOYA is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// VOYA is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.


document.addEventListener("DOMContentLoaded", function () {
    let isFormEdite = false;
    const form = document.getElementById("proposal-form");

    // Select all form elements that could be changed
    const formElements = document.querySelectorAll("input, textarea, select");

    // Detect changes (not just clicks)
    formElements.forEach(element => {
        const originalValue = element.value;

        element.addEventListener("input", function () {
            if (element.value!== originalValue) {
                isFormEdite = true;
            }
        });
    });

    // Warn before leaving
    window.addEventListener("beforeunload", function (event) {
        if (isFormEdite) {
            event.preventDefault();
            event.returnValue = "You have unsaved changes. Are you sure you want to leave?";
        }
    });

    // Reset warning when form is submitted
    form.addEventListener("submit", function () {
        isFormEdite = false;
    });
});