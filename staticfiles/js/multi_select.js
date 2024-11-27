document.addEventListener("DOMContentLoaded", function () {
    console.log("Initializing Select2...");

    // Initialize Select2 on elements with the class "multi-select"
    $('.multi-select').select2({
        placeholder: "Select options",
        allowClear: true,
        closeOnSelect: false // Keep the dropdown open after selecting an option (optional)
    });

    // Function to update the placeholder with the selected count
    function updatePlaceholder(selectElement) {
        const selectedCount = $(selectElement).select2('data').length;
        const placeholderText = selectedCount > 0 ? `${selectedCount} option(s) selected` : "Select options";
        $(selectElement).next('.select2-container').find('.select2-selection__placeholder').text(placeholderText);
    }

    // Initial update of the placeholder for each select element on load
    $('.multi-select').each(function () {
        updatePlaceholder(this);
    });

    // Update the placeholder whenever the selection changes
    $('.multi-select').on('change', function () {
        updatePlaceholder(this);
    });
});