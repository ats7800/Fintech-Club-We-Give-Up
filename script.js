let selectedBtn = "Apple";
let loading = false;

const Chart = document.getElementById("myChart");
// Chart.style.visibility = "hidden";

const buttons = document.getElementsByClassName("stock-button");
const submitBtn = document.getElementById("submitBtn");

submitBtn.addEventListener("click", function () {
  date = document.getElementById("date").value;
  const data = {
    date: date,
    stock: selectedBtn,
  };
  postPredict(data);

  // Convert the input date string to a Date object
  const currDate = new Date(date);

  // Calculate one day later
  currDate.setDate(currDate.getDate() + 1);
  const oneDayLater = formatDate(currDate);

  // Reset the date to the original input date
  currDate.setDate(currDate.getDate() - 1);

  // Calculate five days earlier
  currDate.setDate(currDate.getDate() - 5);
  const fiveDaysEarlier = formatDate(currDate);

  console.log("One day later: ", oneDayLater);
  console.log("Five days earlier: ", fiveDaysEarlier);

  //   fetch(`http://api.marketstack.com/v1/eod
  //     ? access_key = b4c8f9e44087a3ee81d7cf8e06d08782
  //     & symbols = AAPL
  //     & date_from = ${fiveDaysEarlier}
  //     & date_to = ${oneDayLater}`);

  // Chart.style.visibility = "visible";
});

// document.addEventListener("click", function () {
//   senti = sentiArea.value;
//   const data = {
//     senti: senti,
//   };
//   sentiPredict(data);
// });

for (let i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener("click", function () {
    // Remove active class from all buttons
    for (let j = 0; j < buttons.length; j++) {
      buttons[j].classList.remove("active");
    }
    // Add active class to the clicked button
    this.classList.add("active");
    selectedBtn = this.name;
    // console.log(this.name);
  });
}

function postPredict(data) {
  if (loading) return;
  loading = true;
  document.getElementById("loadingIcon").style.display = "inline-block";
  fetch("http://localhost:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Response from server:", data);
      score = data["stock score"];
      const emos = document.getElementsByClassName("rnd1");
      score = parseInt(score);
      for (i in emos) {
        if (emos[i].classList) emos[i].classList.remove("showScore");
      }
      emos[score].classList.add("showScore");
      document.getElementById("loadingIcon").style.display = "none";
      loading = false;
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("loadingIcon").style.display = "none";
      loading = false;
    });
}

function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}
