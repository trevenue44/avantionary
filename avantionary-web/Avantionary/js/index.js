function getInputValue(){
    // Selecting the input element and get its value 
    var inputVal = document.getElementById("search_bar").value;
    console.log(inputVal);
    // Displaying the value
    document.getElementById("outputarea").innerHTML = inputVal;
        //Call Api 
}

function showAnswer(){
    var inputVal = document.getElementById("search_bar").value;
    //var search = document.getElementById("word").value;
        console.log(inputVal);

        var url = `http://127.0.0.1:5000/WordInformation/${inputVal}`
        var word = ""
        console.log("In you");
        axios.get(url)
        .then(response => {
         word = response.data.data;
            console.log(`GET list users`, word);
            if (word[0] == "" || word == "Word does not exist."){
              alert(word)
            }
            else{
              alert(word)
            }

        })
        .catch(error => console.error(error));
    document.getElementById("outputarea").innerHTML = word;
    //alert("Trial Note")
    //Show answer in text area

}


