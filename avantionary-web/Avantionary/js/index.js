function getInputValue(){
    // Selecting the input element and get its value 
    var inputVal = document.getElementById("search_bar").value;
    console.log(inputVal);
    // Displaying the value
    document.getElementById("outputarea").innerHTML = inputVal;
    //alert("Trial Note")
        alert(inputVal);
}

function showAnswer(){
    var inputVal = document.getElementById("search_bar").value;
    document.getElementById("outputarea").innerHTML = inputVal;
    alert("Trial Note")

}


