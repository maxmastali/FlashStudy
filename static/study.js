function goBack() {
  return window.history.back();
}

// wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // enter function if div with a id of "term_visibility" is clicked on
    document.getElementById("term_visibility").onclick = function () {

        // store all the elements with a class name of "term_study_input" into variable "terms"
        var terms = document.getElementsByClassName("term_study_input");

        // all of the terms have the same visibility all the time
        // so if the first term input is visible, make all the term inputs hidden
        if (terms[0].style.visibility === "visible") {

            // repeat over all the term inputs
            for (let i = 0; i < terms.length; i++)
            {
                terms[i].style.visibility = "hidden";
            };

            // and change the content of the div with an id of "term_visibility" to "View Terms"
            document.getElementById("term_visibility").textContent = "View Terms";

            }

        // all of the terms have the same visibility all the time
        // so if the first term input is not visible, make all the term inputs visible
        else {

            // repeat over all the term inputs
            for (let i = 0; i < terms.length; i++)
            {
                terms[i].style.visibility = "visible";
            };

            // and change the content of the div with an id of "term_visibility" to "Hide Terms"
            document.getElementById("term_visibility").textContent = "Hide Terms";
        };

    };

    // enter function if div with a id of "definition_visibility" is clicked on
    document.getElementById("definition_visibility").onclick = function () {

        // store all the elements with a class name of "definition_study_input" into variable "definitions"
        var definitions = document.getElementsByClassName("definition_study_input");

        // all of the definitions have the same visibility all the tim
        // so if the first definition input is visible, make all the definition inputs hidden
        if (definitions[0].style.visibility === "visible") {

            // repeat over all the definition inputs
            for (let i = 0; i < definitions.length; i++)
            {
                definitions[i].style.visibility = "hidden";
            };

            // and change the content of the div with an id of "definition_visibility" to "View Definitions"
            document.getElementById("definition_visibility").textContent = "View Definitions";

            }

        // all of the definitions have the same visibility all the time
        // so if the first definition input is not visible, make all the definition inputs visible
        else {

            // repeat over all the definition inputs
            for (let i = 0; i < definitions.length; i++)
            {
                definitions[i].style.visibility = "visible";
            };

            // and change the content of the div with an id of "definition_visibility" to "Hide Definitions"
            document.getElementById("definition_visibility").textContent = "Hide Definitions";

        };

    };

    // enter function if div with id of "delete" is clicked on
    document.getElementById("delete").onclick = function () {

        // fill the value of the form input with the title of the set that's displayed on study.html
        document.getElementById("study_delete_input").value = document.getElementById("title").textContent;

        // submit the form
        document.getElementById("study_delete_form").submit();
    };

    // enter function if div with id of "edit" is clicked on
    document.getElementById("edit").onclick = function () {

        // fill the value of the form input with the title of the set that's displayed on study.html
        document.getElementById("study_edit_input").value = document.getElementById("title").textContent;

        // submit the form
        document.getElementById("study_edit_form").submit();
    };

});