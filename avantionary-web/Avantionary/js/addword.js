function addWord(){
    // Selecting the input element and get its value 
    var search = document.getElementById("word").value;
    var partofspeech = document.getElementById("partofspeech").value;
    var synonym = document.getElementById("synonym").value;
    var antonym = document.getElementById("antonym").value;

    // class wordStruct{
    // }
    console.log(body);

    var body = [search,partofspeech,synonym,antonym]
    // alert(body)

    var url = `http://127.0.0.1:5000/WordInformation/${search}`
    //  var url = 'http://127.0.0.1:8000/tenants'

//        
      console.log("In you");
      axios.get(url)
      .then(response => {
          const word = response.data.data;
          console.log(`GET list users`, word);
          if (word == "" || word == "Word does not exist."){
            alert("Enter Word. ")
            //Call POST API.
          }
          else{
            alert(`Word already exists: ${word}`)
          }

      })
      .catch(error => console.error(error));
}


