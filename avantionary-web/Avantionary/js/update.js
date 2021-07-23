function sendUpdate(){
    // Selecting the input element and get its value 
    var word = document.getElementById("word").value;
    var partofspeech = document.getElementById("partofspeech").value;
    var synonym = document.getElementById("synonym").value;
    var antonym = document.getElementById("antonym").value;

    // class wordStruct{
    // }
    console.log(body);

    var body = [word,partofspeech,synonym,antonym]
    alert(body)
    // Displaying the value
    // document.getElementById("outputarea").innerHTML = inputVal;
        //Call Api 
}

// function showAnswer(){
//     var inputVal = document.getElementById("search_bar").value;
//     document.getElementById("outputarea").innerHTML = inputVal;
//     //alert("Trial Note")
//     //Show answer in text area

// }



// //Copied POST js for HTML
// const userAction = async () => {
//     const response = await fetch('http://example.com/movies.json', {
//       method: 'POST',
//       body: myBody, // string or object
//       headers: {
//         'Content-Type': 'application/json'
//       }
//     });
//     const myJson = await response.json(); //extract JSON from the http response
//     // do something with myJson
//   }


  //Sample GET js for HTML 
const userAction = async () => {
//   console.log("In you");
//   axios.get(url)
// .then(response => {
// const users = response.data.data;
// console.log(`GET list users`, users);
// })
// .catch(error => console.error(error));
var search = document.getElementById("word").value;
        console.log(search);

        var url = `http://127.0.0.1:5000/WordInformation/${search}`
//        
        console.log("In you");
        axios.get(url)
        .then(response => {
            const word = response.data.data;
            console.log(`GET list users`, word);
            if (word[0] == "" || word == "Word does not exist."){
              alert(word)
            }
            else{
              alert(word)
            }

        })
        .catch(error => console.error(error));
}
 // };


//Button action code
//   button.addEventListener('click', userAction); or <button onclick="userAction()" /> – Brendan McGill Jun 17 '20 at 1:18 

// ItemJSON = '[  {    "Id": 1,    "ProductID": "1",    "Quantity": 1,  },  {    "Id": 1,    "ProductID": "2",    "Quantity": 2,  }]';
