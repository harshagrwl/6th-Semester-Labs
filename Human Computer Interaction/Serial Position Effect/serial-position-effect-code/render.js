const FULL_DASH_ARRAY = 283;
const WARNING_THRESHOLD = 10;
const ALERT_THRESHOLD = 5;

var animals = [];
var first = 0;
var middle = 0;
var end = 0;
var score = 0;
const COLOR_CODES = {
    info: {
        color: "green"
    },
    warning: {
        color: "orange",
        threshold: WARNING_THRESHOLD
    },
    alert: {
        color: "red",
        threshold: ALERT_THRESHOLD
    }
};

const TIME_LIMIT = 10;
let timePassed = 0;
let timeLeft = TIME_LIMIT;
let timerInterval = null;
let remainingPathColor = COLOR_CODES.info.color;

document.getElementById("timer").innerHTML = `
<div class="base-timer">
  <svg class="base-timer__svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <g class="base-timer__circle">
      <circle class="base-timer__path-elapsed" cx="50" cy="50" r="45"></circle>
      <path
        id="base-timer-path-remaining"
        stroke-dasharray="283"
        class="base-timer__path-remaining ${remainingPathColor}"
        d="
          M 50, 50
          m -45, 0
          a 45,45 0 1,0 90,0
          a 45,45 0 1,0 -90,0
        "
      ></path>
    </g>
  </svg>
  <span id="base-timer-label" class="base-timer__label">${formatTime(
    timeLeft
)}</span>
</div>
`;

startTimer();

function onTimesUp() {
    clearInterval(timerInterval);
}

function startTimer() {
    timerInterval = setInterval(() => {
        timePassed = timePassed += 1;
        timeLeft = TIME_LIMIT - timePassed;
        document.getElementById("base-timer-label").innerHTML = formatTime(
            timeLeft
        );
        setCircleDasharray();
        setRemainingPathColor(timeLeft);

        if (timeLeft === 0) {
            onTimesUp();
        }
    }, 1000);
}

function formatTime(time) {
    const minutes = Math.floor(time / 60);
    let seconds = time % 60;

    if (seconds < 10) {
        seconds = `0${seconds}`;
    }

    return `${minutes}:${seconds}`;
}

function setRemainingPathColor(timeLeft) {
    const { alert, warning, info } = COLOR_CODES;
    if (timeLeft <= alert.threshold) {
        document
            .getElementById("base-timer-path-remaining")
            .classList.remove(warning.color);
        document
            .getElementById("base-timer-path-remaining")
            .classList.add(alert.color);
    } else if (timeLeft <= warning.threshold) {
        document
            .getElementById("base-timer-path-remaining")
            .classList.remove(info.color);
        document
            .getElementById("base-timer-path-remaining")
            .classList.add(warning.color);
    }
}

function calculateTimeFraction() {
    const rawTimeFraction = timeLeft / TIME_LIMIT;
    return rawTimeFraction - (1 / TIME_LIMIT) * (1 - rawTimeFraction);
}

function setCircleDasharray() {
    const circleDasharray = `${(
        calculateTimeFraction() * FULL_DASH_ARRAY
    ).toFixed(0)} 283`;
    document
        .getElementById("base-timer-path-remaining")
        .setAttribute("stroke-dasharray", circleDasharray);
}

setTimeout(function () {
    window.location.href = 'game.html';
}, 10000);

function changeColor(el) {
    if (animals.includes(el.textContent)) {
        el.style.fontWeight = "normal";
        const index = animals.indexOf(el.textContent);
        if (index > -1) {
            animals.splice(index, 1);
        }
        if (el.textContent === "Lion" || el.textContent === "Elephant" || el.textContent === "Monkey") {
            first--;
        }
    }
    else {
        console.log(animals);
        el.style.fontWeight = "bold";
        if (animals.length <= 8) {
            animals.push(el.textContent);
        }
        else {
            alert("More than 8 animals selected!");
        }
        if (el.textContent == "Lion" || el.textContent === "Elephant" || el.textContent === "Monkey") {
            first += 1;
        }
        if (el.textContent == "Rabbit" || el.textContent === "Giraffe" || el.textContent === "Dog") {
            end += 1;
        }
        if (el.textContent == "Horse" || el.textContent === "Tiger") {
            middle += 1;
        }
    }
    localStorage.setItem("firstn", first);
    localStorage.setItem("endn", end);
    localStorage.setItem("middlen", middle);
}
function calculateScore() {
    first = parseInt(localStorage.getItem("firstn"));
    middle = parseInt(localStorage.getItem("middlen"));
    end = parseInt(localStorage.getItem("endn"));
    score = first + middle + end;
    if (first >= 2 && end >= 2) {
        document.getElementById("analysis").innerHTML = "Your score is " + score + "/8. You tend to remember the animals in the beginning and at the end of the list.";
    }
    else if (first >= 2) {
        document.getElementById("analysis").innerHTML = "Your score is " + score + "/8. You tend to remember the animals in the beginning  of the list.";
    }
    else if (end >= 2) {
        document.getElementById("analysis").innerHTML = "Your score is " + score + "/8. You tend to remember the animals  at the end of the list.";
    }
    else if (score == 8) {
        document.getElementById("analysis").innerHTML = "You have a perfect score of 8/8. You have a good memory. Serial position effect doesn't apply on you.";
    }
    else {
        document.getElementById("analysis").innerHTML = "Your score is " + score + "/8.";
    }
}