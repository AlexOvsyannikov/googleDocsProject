function sendData(){
    var url_field = document.getElementById('formProvideUrl')
    var url = url_field.value;
    var ready = true;
    if (! url.startsWith('https://docs.google.com/forms')){
        ready = false;
        alert('Check your input');
    }


    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/getForm', true);

    //Передаёт правильный заголовок в запросе
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    xhr.onreadystatechange = function() {//Вызывает функцию при смене состояния.
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {

        }
    }
    if (ready){
        xhr.send(JSON.stringify({ "url": url }));
        url_field.value = '';
    }



}