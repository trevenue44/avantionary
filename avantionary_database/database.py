import json

class DataBase():
    def definitions(word):
        """
        Returns a tuple of (definition, synonyms, antonyms) if word exists.
        
        Returns 'Word does not exist.' if it does not exist.

        Input should be a string.
        """
        word = word.upper().strip()
        first_letter = word[0]
        # knowing the first letter of the word, we can go straight to the json file to open
        if first_letter.isalpha():
            section = "./avantionary_database/dictionary_data/D" + first_letter + ".json"
            with open(section) as sec:
                dictionary_data = json.load(sec)
        else:
            return "Word does not exist."
        # with dic data, we find all info about the word
        if word in dictionary_data:
            word_info = dictionary_data[word]
            word_meanings = word_info["MEANINGS"]
            word_synonyms = ", ".join(syn for syn in word_info["SYNONYMS"] if syn.upper() != word)
            word_antonyms = ", ".join(word_info["ANTONYMS"])
            word_meanings_s = ""
            for key in word_meanings:
                if type(word_meanings[key]) == list:
                    for item in word_meanings[key]:
                        if type(item) == list:
                            for one in item:
                                word_meanings_s = word_meanings_s + "\n" + one
                        else:
                            word_meanings_s = word_meanings_s + "\n" + item

                    word_meanings_s += "\n"
                else:
                    word_meanings_s = word_meanings_s + "\n" + word_meanings[key]
            return (word_meanings_s.strip("\n"), word_synonyms, word_antonyms)
        else:
            return "Word does not exist."


    def add_to_dictionary(info):
        """
        Funtion for adding to the dictionary json files
        """
        first_letter = info["word"][0].upper()
        section = "./avantionary_database/dictionary_data/D" + first_letter + ".json"
        with open(section) as sec:
            all_data = json.load(sec)

        # putting the data into the right form
        processed_info_to_add = {
            "MEANINGS": {"1": info["meaning"]},
            "ANTONYMS": info["antonyms"],
            "SYNONYMS": info["synonyms"]
        } 

        # updating the json file
        all_data[info["word"].upper()] = processed_info_to_add
        json_object = json.dumps(all_data, indent=4, sort_keys=True)

        with open(section, "w") as f:
            f.write(json_object)
        
        return info["word"].upper() + " added succesfully!"


    def delete_from_dictionary(word):
        """
        Funtion for deleting from the dictionary json files
        """
        first_letter = word.upper()[0]
        section = "./avantionary_database/dictionary_data/D" + first_letter + ".json"
        with open(section) as sec:
            all_data = json.load(sec)
        
        if word in all_data:
            del all_data[word.upper()]

            json_object = json.dumps(all_data, indent=4, sort_keys=True)

            with open(section, "w") as f:
                f.write(json_object)
            
            return "Word deleted successfully."

        else:
            return "Word not in dictionary"

