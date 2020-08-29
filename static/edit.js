function goBack() {
  return window.history.back();
}

// wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // enter function if button with id of "edit_button" is clicked on
    document.getElementById("edit_button").onclick = function () {

        // fill the value of the form input with the title of the set that's displayed on edit.html
        document.getElementById("edit_set").value = document.getElementById("title").textContent;
    };

});
