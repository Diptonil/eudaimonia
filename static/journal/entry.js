$(document).ready(function () {
    $("#test").submit(function (event) {
        var iframeDoc;
        const val = document.querySelector('#eName').value;
        if (window.frames && window.frames.textField &&
            (iframeDoc = window.frames.textField.document)) {
            var iframeBody = iframeDoc.body;
            var content = iframeBody.innerHTML;
        }
        $.ajax({
            type: "POST",
            url: "",
            data: { 'csrfmiddlewaretoken': "{{  csrf_token  }}", 'content': content, 'title': val },
            success: function (response) {
                if (response == 1) {
                    window.location = "{% url 'all_entries' %}";
                }
            },
        });
        return false;
    });
});

function popupMessage() {
    var popup = document.querySelector('.popup');
    popup.classList.add('popup-active');
    setTimeout(() => {
        popup.classList.remove('popup-active')
    }, 6000);
}

let img=document.getElementById('display-img');
let button = document.getElementById('button');
button.addEventListener('change', function () {
    img.src= URL.createObjectURL(this.files[0])
    img.style.display='block';
})

textField.document.designMode = 'On';

function executeCmdnull(command) {
    textField.document.execCommand(command, false, null);

}

function executeCmd(command, element) {
    textField.document.execCommand(command, false, null);
    element.classList.toggle("highlight");
}

function executeCmdD(command, element) {
    var elements = document.querySelectorAll('.dd')
    var i = 0
    length = elements.length;
    for (i; i < length; i++) {
        if (elements[i].classList.contains('highlight')) {
            elements[i].classList.remove('highlight');
        }
    }
    textField.document.execCommand(command, false, null);
    console.log(length)
    element.classList.add('highlight');
}

function execCmdWithArg(command, arg) {
    textField.document.execCommand(command, false, arg);

}