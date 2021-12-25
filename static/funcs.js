function sendData(){
    var url_field = document.getElementById('formProvideUrl')
    var url = url_field.value;
    var ready = true;
    if (! url.startsWith('https://docs.google.com/forms')){
        ready = false;
        alert('Check your input');
    }

    // https://docs.google.com/forms/d/e/1FAIpQLSeUvwATpaEkWE_QbE2LtZ9RWXPzJKinubMsHxD4xHrJsgrG6A/viewform
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/getForm', true);

    //Передаёт правильный заголовок в запросе
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    xhr.onreadystatechange = function() {//Вызывает функцию при смене состояния.
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            document.write(xhr.response)
        }
    }
    if (ready){
        xhr.send(JSON.stringify({ "url": url }));
        url_field.value = '';
    }
}

function startVoting(){
    var options_labels = document.getElementsByName('opt');
    var step;
    var options = [];
    var _val;
    var ready = true;
    for (step = 0; step < options_labels.length; step++) {
        _val = options_labels[step].value
        if (_val === ''){
            alert('Все поля должны быть заполнены');
            ready = false;
            break;
        }
        options.push(_val)
    }
    var to_send = {};
    to_send["data"] = options;
    to_send["session"] = document.getElementById('session').textContent;
    to_send['votes'] = document.getElementById('votes').value;
    to_send['sleep'] = document.getElementById('sleep').value;
    if ((to_send['votes'] === '' || to_send['sleep'] === '') && ready === true){
            alert('Все поля должны быть заполнены');
            ready = false;
        }
    if (parseInt(to_send['votes']) < 5){
        alert('Минимальное число голосов - 5!');
        ready = false;
    }


    if (ready){
        var xhr = new XMLHttpRequest();

    xhr.open("POST", '/getProbes', true);

    //Передаёт правильный заголовок в запросе
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    xhr.onreadystatechange = function() {//Вызывает функцию при смене состояния.
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            document.location.href = '/id/' + xhr.response
        }
    }
    xhr.send(JSON.stringify(to_send));
    }

}

function refresh(){

}