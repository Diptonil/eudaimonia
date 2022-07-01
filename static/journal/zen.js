var c, total;
var alertflag;
var timedMessage = document.querySelector(".timedMessage");

function setTime(time){
    timedMessage.innerHTML = "placeholder text(You cannot pause the timer yet)" //text when the user first enters the zen mode
    c = time;
    total = c;
    alertflag = 0;
    
}

var pauseBut = document.querySelector('#pause')
var resume = document.querySelector('#resume')
var breakcd = document.getElementById('BreakCountdown');
pauseBut.disabled = true;
var isPaused = false;
var flag = 0;
var breakPeriod;

//Break Countdown
function startclockBreak(){
    var interval= setInterval(updateCountdownb, 1000);
    function updateCountdownb(){
        --breakPeriod;
        var second = breakPeriod % 60; // Seconds that cannot be written in minutes
        var secondsInMinute = (breakPeriod - second) / 60; // Gives the seconds that COULD be given in minutes
        var minute = secondsInMinute % 60; // Minutes that cannot be written in hours
        var hour = (secondsInMinute - minute) / 60;
        
        breakcd.innerHTML = ` Break Countdown: ${minute}m ${second}s`
        if (breakPeriod == 0) { 
            timedMessage.innerHTML = "It's time to get back to work"
            clearInterval(interval);
        
        }
    }
}

function pauseTimer(){
    breakPeriod = 900;
    isPaused = true;
    pauseBut.style.display ="none"
    resume.style.display ="block"
    timedMessage.innerHTML = "Your are taking a break..."
    pauseBut.disabled = true;
    startclockBreak();
    flag++;
}

function unpauseTimer(){
    isPaused = false;
    resume.style.display ="none"
    pauseBut.style.display ="block"
    breakcd.innerHTML = "";
    timedMessage.innerHTML = "You just completed your break!"
}

//to pass the spent time in Zen mode to add to the total hours or something
function passTime(){
    var seconds = c % 60; // Seconds that cannot be written in minutes
    var minutes = seconds % 60; // Minutes that cannot be written in hours
    var hours = (seconds - minutes) / 60;
}

const countdownEl = document.getElementById('countdown');

var intervalReference;
function startclock(){
    var interval= setInterval(updateCountdown, 1000);
    intervalReference = interval
    function updateCountdown(){
        
        if(!isPaused){

            --c;
            var seconds = c % 60; // Seconds that cannot be written in minutes
            var secondsInMinutes = (c - seconds) / 60; // Gives the seconds that COULD be given in minutes
            var minutes = secondsInMinutes % 60; // Minutes that cannot be written in hours
            var hours = (secondsInMinutes - minutes) / 60;
            
            countdownEl.innerHTML = `${hours}hr ${minutes}m ${seconds}s`
            if (c == 0) { 
                timedMessage.innerHTML = "You were able to stay focused for the set period"
                passTime();
                clearInterval(interval);
            }
            if(c < (total - 3600) && flag==0){
                timedMessage.innerHTML = "You might want to consider taking a break a break now"
                pauseBut.disabled = false
            }
            else if(c < (total - 6300) && flag==1){
                timedMessage.innerHTML = "You might want to consider taking a break a break now"
                pauseBut.disabled = false
            }
            else if(c < (total - 8100) && flag==2){
                timedMessage.innerHTML = "You might want to consider taking a break a break now"
                pauseBut.disabled = false
            }
            else if(c < (total - 9900) && flag==3){
                timedMessage.innerHTML = "You might want to consider taking a break a break now"
                pauseBut.disabled = false
            }
        }
    }
}


// zen mode activate and deactivate
var elem = document.querySelector(".window");
function openFullscreen() {
    if (elem.requestFullscreen) {
        elem.classList.add('active')
        elem.requestFullscreen();
        startclock()
    } else if (elem.webkitRequestFullscreen) { 
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { 
        elem.msRequestFullscreen();
    } else if(document.fullscreenElement){
        elem.classList.remove('active')
    }
}

function closeFullscreen() {
    if (document.exitFullscreen) {
        if (c != 0 && alertflag == 0){
            timedMessage.innerHTML = "You will lose the total time spent in Zen mode from being considered if you exit now. Click on exit again if you want to continue"
            alertflag++;
        } else{
            document.exitFullscreen();
            location.reload(true)
            clearInterval(intervalReference);
            elem.classList.remove('active')
        }
    } 
}