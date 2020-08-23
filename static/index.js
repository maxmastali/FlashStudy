// wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // store an array of all the elements with a class of "titles" in variable "titles"
    let titles = document.getElementsByClassName("titles");

    // repeat for all the titles displayed on index.html
    for (let i = 0; i < titles.length; i++)
    {
        // create an onclick event function for when the ith element is clicked on
        titles[i].onclick = function()  {

            // fill the value of the form input with the value of the ith element (of which has been clicked on)
            document.getElementById("index_input").value = titles[i].value;

            // submit the form
            document.getElementById("index_form").submit();
        };

    };

});
