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
      var url = "https://learnappmaking.com/ex/news/articles/Apple?secret=CHWGk3OTwgObtQxGqdLvVhwji6FsYm95oe87o3ju"
    const response = await fetch(url);
    const myJson = await response.json(); //extract JSON from the http response
    // do something with myJson
    console.log(myJson);
  }


//Button action code
//   button.addEventListener('click', userAction); or <button onclick="userAction()" /> – Brendan McGill Jun 17 '20 at 1:18 

// ItemJSON = '[  {    "Id": 1,    "ProductID": "1",    "Quantity": 1,  },  {    "Id": 1,    "ProductID": "2",    "Quantity": 2,  }]';
