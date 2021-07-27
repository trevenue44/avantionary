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
        console.log(inputVal);

        var url = `http://127.0.0.1:5000/WordInformation/${inputVal}`
        var word = ""
        console.log("In you");
        axios.get(url)
        .then(response => {
          const word = response.data.data;
          console.log(`GET list users`, word);
            alert(`${inputVal} : \n \n \n ${word}`)
            // if (word == "" || word == "Word does not exist."){
            //   alert(word)
            // }
            // else{
            //   document.getElementById("outputarea").innerHTML = word;
            // }

        })
        .catch(error => console.error(error));
    // document.getElementById("outputarea").innerHTML = word;
    // document.getElementById("outputarea").innerHTML = inputVal;
    //alert("Trial Note")
    //Show answer in text area

}


