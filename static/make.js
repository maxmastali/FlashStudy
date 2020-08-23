// variable "i" used to make sure at least one flashcard is left on make.html
var i = 10;

// wait for page to load
document.addEventListener('DOMContentLoaded', function() {

    // set an onclick function for the div with the id of "remove0"
    document.getElementById('remove0').onclick = function () {

        // enter if i > 1
        if (i > 1) {

            // remove the 0th flashcard
            document.querySelector('#flashcard0').remove();

            // decrement i by 1
            i--;

            // return nothing in order to exit the function
            return;
        };

        // let user know that they must create at least one flashcard
        alert("Must submit at least one flashcard!");

        // return nothing in order to exit the function
        return;
    };

    // repeat for the 1st flashcard
    document.getElementById('remove1').onclick = function () {
        if (i > 1) {
            document.querySelector('#flashcard1').remove();
            i--;
            return;
        };
        alert("Must submit at least one flashcard!");
        return;
    };

    // repeat for the 2nd flashcard
    document.getElementById('remove2').onclick = function () {
        if (i > 1) {
            document.querySelector('#flashcard2').remove();
            i--;
            return;
        };
        alert("Must submit at least one flashcard!");
        return;
    };

    // repeat for the 3rd flashcard
    document.getElementById('remove3').onclick = function () {
        if (i > 1) {
            document.querySelector('#flashcard3').remove();
            i--;
            return;
        };
        alert("Must submit at least one flashcard!");
        return;
    };

    // repeat for the 4th flashcard
    document.getElementById('remove4').onclick = function () {
        if (i > 1) {
            document.querySelector('#flashcard4').remove();
            i--;
            return;
        };
        alert("Must submit at least one flashcard!");
        return;
    };

    // repeat for the 5th flashcard
    document.getElementById('remove5').onclick = function () {
        if (i > 1) {
            document.querySelector('#flashcard5').remove();
            i--;
            return;
        };
        alert("Must submit at least one flashcard!");
        return;
    };

    // repeat for the 6th flashcard
    document.getElementById('remove6').onclick = function () {
        if (i > 1) {
            document.querySelector('#flashcard6').remove();
            i--;
            return;
        };
        alert("Must submit at least one flashcard!");
        return;
    };

    // repeat for the 7th flashcard
    document.getElementById('remove7').onclick = function () {
        if (i > 1) {
            document.querySelector('#flashcard7').remove();
            i--;
            return;
        };
        alert("Must submit at least one flashcard!");
        return;
    };

    // repeat for the 8th flashcard
    document.getElementById('remove8').onclick = function () {
        if (i > 1) {
            document.querySelector('#flashcard8').remove();
            i--;
            return;
        };
        alert("Must submit at least one flashcard!");
        return;
    };

    // repeat for the 9th flashcard
    document.getElementById('remove9').onclick = function () {
        if (i > 1) {
            document.querySelector('#flashcard9').remove();
            i--;
            return;
        };
        alert("Must submit at least one flashcard!");
        return;
    };

});
