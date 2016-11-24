function run(input, parameters) {

    var links = /((?:https\:\/\/)|(?:http\:\/\/)|(?:www\.))?([^a-z ]\ *([0-9.,])*\d)?([a-zA-Z0-9@\-\.]+\.[a-zA-Z]{2,3}(?:\??)[a-zA-Z0-9\-\._\?\,\'\/\\\+&%\$#\=~]+)/;
    var numbers = /(\d*\.)+(.\d*)/gm;
    var references = /(.*)(\((.*?)\))/;
    var years = /([(]\d*[)])|(\, \d*)/gm;
    var asciicrap = /(-|_|\||\\|[)]|[(]|[/]|‘|`)\B(\s|-|_|\||,|\\|[)]|[(]|[/]|‘|`|V|[.]|\d*)*/gm;
    var sentences = input[0].replace(/\s\s+/g, ' ').replace(asciicrap,'').replace(/([.?!])\s*(?=[A-Z])/g, "$1|").split("|");


    for (var i = 0; i < sentences.length; i++) {
        //sentence filters (ascii art, numberlines, links, sentences)
        if ((links.test(sentences[i])) || (sentences[i] == '"') || (sentences[i] == " ")) {
            sentences[i] = "";
        } else if (numbers.test(sentences[i])){
            sentences[i].replace(numbers, ''); //filter out loose number starts
        } else {
            //remove linebreaks
            sentences[i].replace('/- /','');
            //split into words
            var words = sentences[i].split(" ");

            for (var j = 0; j < words.length; j++) {
                //loose starts
                if ((words[j].charAt(0) == " ") || (words[j].charAt(0) == '"') || (words[j] == '>>')) {
                    sentences[i] = words.pop(); //take out first character, place back into original array
                //word filters (test on only numbers, links, references, loose sentences)
                } else if ((numbers.test(words[j])) || (links.test(words[j])) || (references.test(words[j])) || (words.length < 2)) {
                    sentences[i] = "";
                }
            }
            if (years.test(words[words.length])) {
                sentences[i] = "";
            }
        }
    }
    return sentences.join(' ');
}
