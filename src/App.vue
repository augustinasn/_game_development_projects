<template>
  <div id="app" :key="componentKey">
    <div id="nav">
      <a href="http://www.gjensidige.lt" target="_blank">
        <img src="./assets/gjen.png" alt="Gjensidige logo" />
      </a>
      <div id="lang-change">
        <select name="lang" id="lang" v-model="lang">
          <option value="lt" selected>LT</option>
          <option value="en">EN</option>
        </select>
        <img :src="'./src/assets/' + lang + '.png'" alt="flag" />
      </div>
    </div>
    <div v-if="!running" id="setup-game">
      <div id="header">
        <h1>
          „
          <span class="emphasised-text">FizzBuzzBazz</span>
          “ {{ strings[lang]["title"] }}
        </h1>
      </div>

      <div id="input-name-div">
        <div id="row-one">
          <input
            id="name-input"
            type="text"
            :style="'border-color:' + borderColor + ';'"
            v-model="playerName"
            :placeholder="strings[lang]['inputName']"
            autofocus
          />
          <a id="start-game-btn" href="#" @click="startGame">{{ strings[lang]["startGame"] }}</a>
        </div>
        <div id="row-two">
          <a href="#" @click="showInstructions">{{ strings[lang]['howToPlay'] }}</a>
        </div>
      </div>
    </div>
    <div id="play-game" v-else>
      <div id="time-bar" :style="'width: ' + timeWidth + '%;'"></div>
      <div id="game-div" v-if="!gameOver">
        <div id="panel">
          <p class="emphasised-text">{{ panelContent }}</p>
        </div>
        <div id="user-input">
          <h2>
            {{ strings[lang]["usrInp"] }}:
            <span class="emphasised-text">{{ userInput }}</span>
          </h2>
          <div id="buttons">
            <button
              id="fizz-btn"
              href="#"
              :style="userFizz ? 'background: #ffd700' : 'background: #f0f8ff'"
              @click="clickFizz"
            >
              &#8592;
              <br />Fizz
              <br />2
            </button>
            <button
              id="buzz-btn"
              href="#"
              :style="userBuzz ? 'background: #ffd700' : 'background: #f0f8ff'"
              @click="clickBuzz"
            >
              &#8593;
              <br />Buzz
              <br />3
            </button>
            <button
              id="bazz-btn"
              href="#"
              :style="userBazz ? 'background: #ffd700' : 'background: #f0f8ff'"
              @click="clickBazz"
            >
              &#8594;
              <br />Bazz
              <br />5
            </button>
          </div>
        </div>
      </div>
      <div id="game-over" v-if="gameOver">
        <h2>
          {{ strings[lang]["usrScore"] }}:
          <span class="emphasised-text">{{ currentNumber }}</span>
        </h2>
        <div id="scores-div">
          <h3 class="emphasised-text">{{ strings[lang]['scores'] }}:</h3>
          <ul id="scores-ul">
            <li
              v-for="score in scores"
              :class="score['name'] == playerName && score['score'] == currentNumber ? 'emphasised-text' : ''"
            >
              <span>{{ score['name'] }}</span>
              <span>{{ score['score'] }}</span>
            </li>
          </ul>
        </div>
        <a id="start-game-btn" href="#" @click="playAgain">{{ strings[lang]["playAgain"] }}</a>
      </div>
    </div>
    <div id="bw-overlay" @click.self="closeInstructions">
      <div id="instruction-modal">
        <nav>
          <i class="fas fa-times emphasised-text" @click="closeInstructions"></i>
        </nav>
        <div id="instructions-content">
          <div id="image-div">
            <img src="./assets/instruction.gif" alt="instructions" />
          </div>
          <div id="text-div">
            <p>{{ strings[lang]['instruction'] }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import db from "./firebase/firebase.js";

export default {
  name: "app",
  data() {
    return {
      firstRun: true,
      componentKey: 0,
      playerName: "",
      running: false,
      panelContent: "...",
      currentNumber: 1,
      userFizz: false,
      userBuzz: false,
      userBazz: false,
      gameOver: false,
      interval: {},
      timeWidth: 0,
      lang: "lt",
      strings: {
        lt: {
          title: "iššūkis",
          inputName: "Įvesk savo vardą",
          startGame: "Pradėti",
          ready: "Pasiruošti",
          steady: "Dėmesio",
          go: "Pirmyn",
          usrInp: "Tavo pasirinkimas",
          usrScore: "Tavo rezultatas",
          playAgain: "Į pradžią",
          scores: "Rezultatų lentelė",
          howToPlay: "Spausk čia, kad pamatytum žaidimo instrukciją.",
          instruction:
            "Žaidimo tikslas - naturalių, iš eilės einančių, skaičių sekoje, kiekvienam skaičiui (nuspalvotam geltonai) nurodyti daliklius su kuriais rezultatas yra be liekanos. Galimi dalikliai: 2 (Fizz), 3 (Buzz), 5 (Bazz). Teisingų variantų gali būti daugiau nei vienas, taip pat gali būti nei vieno. Galite naudoti pelę arba klavietūrą. Sekmės!"
        },
        en: {
          title: "challenge",
          inputName: "Enter your name",
          startGame: "Start",
          ready: "Ready",
          steady: "Steady",
          go: "Go",
          usrInp: "Your input",
          usrScore: "Your result",
          playAgain: "To main",
          scores: "Scoreboard",
          howToPlay: "Click here to see the game instructions.",
          instruction:
            "The goal of the game is - for each natural number in a consecutive sequence (colored yellow) to specify  whether it's evenly divisible by any of given divisors. Available divisors: 2 (Fizz), 3 (Buzz), 5 (Bazz). There may be more than one correct option, and there may be none. You can use either a mouse or a keyboard. Good luck!"
        }
      },
      scores: []
    };
  },
  methods: {
    showInstructions() {
      $("#bw-overlay").css("visibility", "visible");
      console.log("open");
    },
    closeInstructions() {
      $("#bw-overlay").css("visibility", "hidden");
      console.log("close");
    },
    recordResult() {
      db.collection("scores").add({
        name: this.playerName,
        score: this.currentNumber
      });
    },
    populateScores() {
      this.scores = [];

      db.collection("scores")
        .orderBy("score", "desc")
        .limit(10)
        .get()
        .then(qS =>
          qS.forEach(doc => {
            const data = {
              id: doc.id,
              name: doc.data()["name"],
              score: doc.data()["score"]
            };
            this.scores.push(data);
          })
        );
    },
    greenBg() {
      $("html, body").css("background", "#00ff00");

      setTimeout(() => {
        $("html, body").css("background", "#0e2f44");
      }, 500);
    },
    startGame() {
      if (this.playerName !== "") {
        $("#setup-game").addClass("animated fadeOut 1s");

        setTimeout(() => {
          $("#setup-game").removeClass("animated fadeOut 1s");
          this.running = true;
          this.countdown();
        }, 1000);
      }
    },
    countdown() {
      if (this.firstRun) {
        $(document).keydown(e => {
          if (e.which == 37) {
            console.log("Fizz");
            $("#fizz-btn")[0].click();
          } else if (e.which == 38) {
            console.log("Buzz");
            $("#buzz-btn")[0].click();
          } else if (e.which == 39) {
            console.log("Bazz");
            $("#bazz-btn")[0].click();
          }
        });
      }

      setTimeout(() => {
        this.panelContent = this.strings[this.lang]["ready"] + "...";
      }, 1000);

      setTimeout(() => {
        this.panelContent = this.strings[this.lang]["steady"] + "...";
      }, 2500);

      setTimeout(() => {
        this.panelContent = this.strings[this.lang]["go"] + "!";
      }, 4000);

      setTimeout(() => {
        this.step();
      }, 5000);
    },
    step() {
      this.panelContent = this.currentNumber;
      this.resetInputs();
      this.resetTimeBar();

      setTimeout(() => {
        if (this.check()) {
          this.greenBg();

          setTimeout(() => {
            this.currentNumber++;
            this.step();
          }, 500);
        } else {
          this.recordResult();
          $("html, body").css("background", "#ff4040");

          setTimeout(() => {
            this.populateScores();
            this.gameOver = true;
          }, 1000);
        }
      }, 2000);
    },
    resetTimeBar() {
      this.timeWidth = 100;
      clearInterval(this.interval);

      this.interval = setInterval(() => {
        this.timeWidth = this.timeWidth - 1;
      }, 20);
    },
    clickFizz() {
      this.userFizz = !this.userFizz;
    },
    clickBuzz() {
      this.userBuzz = !this.userBuzz;
    },
    clickBazz() {
      this.userBazz = !this.userBazz;
    },
    resetInputs() {
      this.userFizz = false;
      this.userBuzz = false;
      this.userBazz = false;

      $("html, body").css("background", "#0e2f44");
    },
    check() {
      if (
        this.userFizz == this.actualFizz &&
        this.userBuzz == this.actualBuzz &&
        this.userBazz == this.actualBazz
      ) {
        return true;
      } else {
        return false;
      }
    },
    playAgain() {
      $("#play-game").removeClass("animtated fadeIn 1s");
      $("#setup-game").removeClass("animtated fadeIn 1s");

      this.resetInputs();
      this.currentNumber = 1;
      this.panelContent = "...";
      this.playerName = "";
      this.gameOver = false;
      this.running = false;
      this.firstRun = false;

      setTimeout(() => {
        $("#name-input").focus();
      }, 300);
    }
  },
  computed: {
    userInput() {
      return (
        "Fizz".repeat(this.userFizz ? 1 : 0) +
        "Buzz".repeat(this.userBuzz ? 1 : 0) +
        "Bazz".repeat(this.userBazz ? 1 : 0)
      );
    },
    actualFizz() {
      return this.currentNumber % 2 == 0;
    },
    actualBuzz() {
      return this.currentNumber % 3 == 0;
    },
    actualBazz() {
      return this.currentNumber % 5 == 0;
    },
    borderColor() {
      return this.playerName == "" ? "#ff0000" : "#00ff00";
    }
  },
  mounted() {
    $(document).keydown(function(e) {
      if (e.which == 13 && !this.running) {
        $("#start-game-btn")[0].click();
      }
    });
  }
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css?family=Open+Sans&display=swap");
@import url("https://fonts.googleapis.com/css?family=Montserrat&display=swap");

$font-main: "Open Sans", sans-serif;
$font-alt: "Montserrat", sans-serif;
$color-white: #f0f8ff;
$color-black: #133337;
$color-green: #0e2f44;
$color-green-alt: #00ff00;
$color-yellow: #ffd700;
$color-yellow-alt: #ffa500;
$color-red: #ff4040;
$color-red-alt: #ff0000;

* {
  font-family: $font-alt;

  html,
  body {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    color: $color-white;
    background: $color-green;
    transition: background 0.3s;
  }

  .emphasised-text {
    color: $color-yellow;
    background: linear-gradient(to bottom, $color-yellow, $color-yellow-alt);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
}

#nav {
  box-sizing: border-box;
  height: 10vh;
  padding: 0 3rem;
  width: 100%;
  // text-align: right;
  display: flex;
  justify-content: space-between;
  align-items: center;

  img {
    height: 6vh;
    width: auto;
  }

  #lang-change {
    display: flex;
    width: 6rem;
    height: 100%;
    margin-left: auto;
    align-items: center;

    select {
      height: 4vh;
      width: 4rem;
      padding: 0.25rem;
      border: 2px solid $color-yellow;
      color: $color-yellow;
      border-radius: 5px;
      background: none;
      outline: none;
    }

    img {
      width: auto;
      height: 4vh;
      margin-left: 0.5rem;
    }
  }
}

#setup-game {
  // background: black;
  width: 80vw;
  height: 80vh;
  margin: 0 auto;

  background: lighten($color-green, 1%);
  border: solid 5px transparent;
  box-shadow: -3px -3px 13px 3px lighten($color-green, 4%),
    4px 4px 15px 6px darken($color-green, 9%);

  display: flex;
  flex-direction: column;
  align-items: center;

  #header {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;

    h1 {
      font-size: 6rem;
    }
  }

  #input-name-div {
    flex: 1;

    #row-one {
      display: flex;

      input {
        font-family: $font-main;
        border: 5px solid $color-yellow;
        padding: 0.75rem;
        width: 25rem;
        height: 3rem;
        font-size: 2rem;
        line-height: 3rem;
        transition: border-color 0.3s;
        outline: none;
      }

      a {
        display: block;
        background: $color-red;
        text-decoration: none;
        padding: 0.75rem 1.25rem;
        font-size: 2rem;
        color: $color-black;
        height: 3.65rem;
        line-height: 3.65rem;
        margin-left: 0.5rem;

        &:hover {
          background: $color-red-alt;
        }
      }
    }
    #row-two {
      text-align: center;
      height: 3rem;

      a {
        line-height: 3rem;
        font-size: 1rem;
        text-decoration: none;
        color: $color-yellow;
      }
    }
  }
}

#play-game {
  width: 80vw;
  height: 80vh;
  margin: 0 auto;

  background: lighten($color-green, 1%);
  border: solid 5px transparent;
  box-shadow: -3px -3px 13px 3px lighten($color-green, 4%),
    4px 4px 15px 6px darken($color-green, 9%);

  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;

  #time-bar {
    position: absolute;
    top: 0;
    left: 0;
    height: 1vh;
    width: 100%;
    margin-right: auto;
    background: linear-gradient(to bottom, $color-yellow, $color-yellow-alt);
    border-radius: 5px;
  }

  #game-div {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;

    #panel {
      width: 100%;
      height: 50%;
      display: flex;
      align-items: center;
      justify-content: center;

      p {
        font-size: 10rem;
        text-align: center;
        margin: 0;
      }
    }

    #user-input {
      height: 50%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      h2 {
        width: 33%;
        text-align: left;
      }

      #buttons {
        display: flex;
        justify-content: center;

        button {
          border: none;
          background: $color-white;
          border-radius: 5px;
          font-size: 2rem;
          width: 10rem;
          height: 10rem;
          margin: 0 0.5rem;
          transition: background 0.3s;
        }
      }
    }
  }

  #game-over {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    align-items: center;
    justify-content: center;

    h2 {
      font-size: 3rem;
    }

    #scores-div {
      border: 2px solid $color-yellow;
      width: 25%;
      height: 50%;
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      padding: 1.5rem 1rem;

      h3 {
        font-size: 1.5rem;
      }

      ul {
        list-style-type: none;
        width: 75%;
        display: flex;
        flex-direction: column;
        padding: 0;
        margin: 0;
        // margin-left: 0;
        // margin-right: 16px;

        li {
          list-style-type: none;
          display: flex;
          margin-bottom: 0.5rem;
          justify-content: space-between;
          border-bottom: 1px dotted $color-yellow;
        }
      }
    }

    a {
      display: block;
      background: $color-red;
      text-decoration: none;
      padding: 0.5rem 1.25rem;
      font-size: 1.5rem;
      color: $color-black;
      height: 3.65rem;
      line-height: 3.65rem;
      margin-top: 2rem;
      margin-left: 0.5rem;
      transition: background 0.3s;

      &:hover {
        background: $color-red-alt;
        transition: background 0.3s;
      }
    }
  }
}

#bw-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  visibility: hidden;
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;

  #instruction-modal {
    width: 75%;
    height: 75%;
    background: $color-white;
    border-radius: 5px;

    nav {
      box-sizing: border-box;
      width: 100%;
      height: 10%;
      text-align: right;
      padding: 0 1rem;

      i {
        line-height: 4rem;
        font-size: 2rem;
        cursor: pointer;
      }
    }

    #instructions-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 90%;

      #image-div {
        flex: 2;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;

        img {
          border: 5px solid $color-yellow;
          height: 100%;
          width: auto;
        }
      }

      #text-div {
        flex: 1;
        width: 50%;
        display: flex;
        align-items: center;
        justify-content: center;

        p {
          color: $color-black;
          text-align: justify;
        }
      }
    }
  }
}
</style>
