// Form field visibility toggle functions
// These functions handle showing/hiding form fields based on select/input values

$(document).ready(function() {
    // Generalized function to show/hide elements based on select/input value
    // Usage: toggleElementVisibility(triggerSelector, targetSelector, showValue, hideValue, containerSelector)
    // Parameters:
    //   triggerSelector: jQuery selector for the element that triggers the show/hide (e.g., '#author_alive')
    //   targetSelector: jQuery selector for the element to show/hide (e.g., '#death-year' or '#performance_phonogram_available_year')
    //   showValue: value that triggers showing the target (e.g., 'author_dead')
    //   hideValue: optional - if provided, only hides when this value is selected (otherwise hides for all other values)
    //   containerSelector: optional - if provided, hides the container div that includes the label (e.g., parent div with class)
    //                              If not provided, hides the targetSelector itself (which should be a container div)
    function toggleElementVisibility(triggerSelector, targetSelector, showValue, hideValue, containerSelector) {
        $(triggerSelector).change(function() {
            var currentValue = $(this).val();
            var shouldShow = (currentValue === showValue);
            
            // Determine what to show/hide
            var elementToToggle = containerSelector ? $(containerSelector) : $(targetSelector);
            
            if (shouldShow) {
                elementToToggle.show();
            } else if (hideValue !== undefined && currentValue === hideValue) {
                elementToToggle.hide();
            } else if (hideValue === undefined) {
                elementToToggle.hide();
            }
        });
        
        // Trigger on page load to set initial state
        $(triggerSelector).trigger('change');
    }

    // Alternative: More flexible version that accepts multiple show values
    // Usage: toggleElementVisibilityMultiple(triggerSelector, targetSelector, showValues, containerSelector)
    //   showValues: array of values that trigger showing (e.g., ['value1', 'value2'])
    //   containerSelector: optional - if provided, hides the container div that includes the label
    //                         If not provided, automatically finds the parent .mb-3 container (includes label)
    function toggleElementVisibilityMultiple(triggerSelector, targetSelector, showValues, containerSelector) {
        $(triggerSelector).change(function() {
            var currentValue = $(this).val();
            
            // If containerSelector is provided, use it; otherwise find parent .mb-3 container
            var elementToToggle;
            if (containerSelector) {
                elementToToggle = $(containerSelector);
            } else {
                // Automatically find the parent .mb-3 container that includes the label
                elementToToggle = $(targetSelector).closest('.mb-3');
            }
            
            if (showValues.includes(currentValue)) {
                elementToToggle.show();
            } else {
                elementToToggle.hide();
            }
        });
        
        // Trigger on page load to set initial state
        $(triggerSelector).trigger('change');
    }

    // Helper function: Hide field and its label by finding the parent container
    // Usage: toggleElementVisibilityWithLabel(triggerSelector, fieldSelector, showValue)
    // This automatically finds the parent .mb-3 div that contains both the label and the field
    function toggleElementVisibilityWithLabel(triggerSelector, fieldSelector, showValue) {
        $(triggerSelector).change(function() {
            var currentValue = $(this).val();
            // Find the parent container div (usually .mb-3) that contains both label and field
            var container = $(fieldSelector).closest('.mb-3');
            
            if (currentValue === showValue) {
                container.show();
            } else {
                container.hide();
            }
        });
        
        // Trigger on page load to set initial state
        $(triggerSelector).trigger('change');
    }

    // ============================================
    // TOGGLE FUNCTION USAGE
    // ============================================

    // Shows the author death year if author is not alive
    toggleElementVisibility('#author_alive', '#death-year', 'author_dead');
    
    // These hide the year fields if the corresponding mode of availability is not selected
    toggleElementVisibilityWithLabel('#performance_phonogram_available', '#performance_phonogram_available_year', 'performance_phonogram_available');
    toggleElementVisibilityWithLabel('#performance_fixed_not_phonogram_available', '#performance_fixed_not_phonogram_available_year', 'performance_fixed_not_phonogram_available');

    toggleElementVisibilityWithLabel('#phonogram_published_fixed_medium', '#phonogram_published_fixed_medium_year', 'phonogram_published_fixed_medium');
    toggleElementVisibilityWithLabel('#phonogram_available_no_medium', '#phonogram_available_no_medium_year', 'phonogram_publically_available_no_medium');

    toggleElementVisibilityWithLabel('#film_fixation_published_fixed_medium', '#film_fixation_published_fixed_medium_year', 'film_fixation_published_fixed_medium');
    toggleElementVisibilityWithLabel('#film_fixation_available_no_medium', '#film_fixation_available_no_medium_year', 'film_fixation_publically_available_no_medium');

    toggleElementVisibilityWithLabel('#press_publication', '#press_publication_year', 'press_publication');

    // These hide CC license and rights acquired fields if the institution is a rightholder
    toggleElementVisibilityMultiple('#current_rightholder', '#object_cc_license', ['rightholder_unknown', 'rightholder_not_us', 'uncertain']); 
    toggleElementVisibilityMultiple('#current_rightholder', '#object_copyright_rights_acquired_to_make_available', ['rightholder_unknown', 'rightholder_not_us', 'uncertain']); 

    toggleElementVisibilityMultiple('#performance_current_rightholder', '#performance_cc_license', ['rightholder_unknown', 'rightholder_not_us', 'uncertain']); 
    toggleElementVisibilityMultiple('#performance_current_rightholder', '#performance_rights_acquired_to_make_available', ['rightholder_unknown', 'rightholder_not_us', 'uncertain']); 

    toggleElementVisibilityMultiple('#phonogram_current_rightholder', '#phonogram_cc_license', ['rightholder_unknown', 'rightholder_not_us', 'uncertain']); 
    toggleElementVisibilityMultiple('#phonogram_current_rightholder', '#phonogram_rights_acquired_to_make_available', ['rightholder_unknown', 'rightholder_not_us', 'uncertain']); 

    toggleElementVisibilityMultiple('#film_fixation_current_rightholder', '#film_fixation_cc_license', ['rightholder_unknown', 'rightholder_not_us', 'uncertain']); 
    toggleElementVisibilityMultiple('#film_fixation_current_rightholder', '#film_fixation_rights_acquired_to_make_available', ['rightholder_unknown', 'rightholder_not_us', 'uncertain']); 

    toggleElementVisibilityMultiple('#broadcast_current_rightholder', '#broadcast_cc_license', ['rightholder_unknown', 'rightholder_not_us', 'uncertain']); 
    toggleElementVisibilityMultiple('#broadcast_current_rightholder', '#broadcast_rights_acquired_to_make_available', ['rightholder_unknown', 'rightholder_not_us', 'uncertain']); 

    // These hide rightholder/CC license and rights acquired fields if the digital representation is not protected
    toggleElementVisibilityMultiple('#digital_repr_ip_rights-copyright', '#digital_repr_copyright_current_rightholder', ['yes', 'uncertain']);
    toggleElementVisibilityMultiple('#digital_repr_ip_rights-copyright', '#digital_repr_copyright_cc_license', ['yes', 'uncertain']);
    toggleElementVisibilityMultiple('#digital_repr_ip_rights-copyright', '#digital_repr_copyright_rights_acquired', ['yes', 'uncertain']);

    toggleElementVisibilityMultiple('#digital_repr_ip_rights-phonogram_rights', '#digital_repr_phonogram_current_rightholder', ['yes', 'uncertain']);
    toggleElementVisibilityMultiple('#digital_repr_ip_rights-phonogram_rights', '#digital_repr_phonogram_cc_license', ['yes', 'uncertain']);
    toggleElementVisibilityMultiple('#digital_repr_ip_rights-phonogram_rights', '#digital_repr_phonogram_rights_acquired', ['yes', 'uncertain']);

    toggleElementVisibilityMultiple('#digital_repr_ip_rights-film_fixation_rights', '#digital_repr_film_fixation_current_rightholder', ['yes', 'uncertain']);
    toggleElementVisibilityMultiple('#digital_repr_ip_rights-film_fixation_rights', '#digital_repr_film_fixation_cc_license', ['yes', 'uncertain']);
    toggleElementVisibilityMultiple('#digital_repr_ip_rights-film_fixation_rights', '#digital_repr_film_fixation_rights_acquired', ['yes', 'uncertain']);

    toggleElementVisibilityMultiple('#digital_repr_ip_rights-other_ip_rights', '#digital_repr_other_current_rightholder', ['yes', 'uncertain']);
    toggleElementVisibilityMultiple('#digital_repr_ip_rights-other_ip_rights', '#digital_repr_other_cc_license', ['yes', 'uncertain']);
    toggleElementVisibilityMultiple('#digital_repr_ip_rights-other_ip_rights', '#digital_repr_other_rights_acquired', ['yes', 'uncertain']);
});

