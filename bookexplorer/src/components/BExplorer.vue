<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" app>
      <v-list dense>
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-contact-mail</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Logged in as {{username}}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link @click="logout">
          <v-list-item-action>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <!-- top app bar -->
    <v-app-bar app color="indigo" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>
        <h2>BookExplorer</h2>
      </v-toolbar-title>
    </v-app-bar>
    <template>
      <div class="text-center ma-2">
        <v-snackbar top v-model="status">
          <h3>{{ message }}</h3>
          <v-btn color="pink" text @click="status = false">Close</v-btn>
        </v-snackbar>
      </div>
    </template>
    <!-- content of the website -->
    <v-content>
      <v-container class="fill-height" fluid>
        <!-- Search bar -->
        <v-row>
          <v-col class="d-flex">
            <v-text-field placeholder="Search..." type="text" v-model="searchfield" />
          </v-col>

          <v-col class="d-flex">
            <v-select :items="items" placeholder="Search Type" v-model="option"></v-select>
          </v-col>

          <v-col class="d-flex">
            <v-btn @click="booksearch">
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <!-- Table to show search results -->
        <v-row align="center" justify="center">
          <v-data-table
            :headers="headers"
            :items="response"
            :items-per-page="10"
            class="elevation-1"
            @click:row="handleClick"
          ></v-data-table>
        </v-row>
      </v-container>
      <!-- Book Page when user clicks on book in table -->
      <template>
        <v-row justify="center">
          <v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
            <v-card>
              <v-toolbar dark color="indigo">
                <v-btn icon dark @click="dialog = false">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
                <v-toolbar-title>
                  <h2>{{ selected_book.title }}, ({{selected_book.isbn}})</h2>
                </v-toolbar-title>
              </v-toolbar>
              <div class="register-box">
                <h2>Written by {{selected_book.author }}, {{selected_book.year}}</h2>
                <br />
                <!-- goodreads api, get reviews and score -->
                <h3>Average rating on Goodreads</h3>
                <v-rating v-model="rating.avg_rating" readonly></v-rating>
                <h3>{{ rating.avg_rating }} / 5 ({{rating.no_rating}} ratings)</h3>
                <br />
                <v-btn color="indigo" dark @click="submit_review">submit a review</v-btn>
              </div>
              <br />
              <!-- display reviews -->
              <v-row align="center" justify="center">
                <v-data-table
                  :headers="headers_book"
                  :items="response_review"
                  :items-per-page="10"
                  class="elevation-1"
                ></v-data-table>
              </v-row>
            </v-card>
          </v-dialog>
        </v-row>
      </template>
      <!-- review dialogue -->
      <template>
        <v-row justify="center">
          <v-btn color="indigo" dark @click.stop="rev_dialog = true">Open Dialog</v-btn>

          <v-dialog v-model="rev_dialog" max-width="40%" hide-overlay>
            <v-card>
              <v-card-title class="headline">Write a Review!</v-card-title>
              <v-textarea 
                counter="250" 
                filled 
                outlined 
                v-model="user_review"
                :maxlength="250"
                class="pa-5"
              ></v-textarea>
              <v-card-text>Let other users know what you think of the book! Did you love it? Did you hate it? Don't be afraid to be honest.</v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green darken-1" text @click="rev_dialog = false">submit</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>
      </template>
    </v-content>
  </v-app>
</template>

<script>
import axios from "axios";
import { eventBus } from "../main.js";
export default {
  name: "BExplorer",
  data: () => ({
    message: "If you are seeing this, there has been a problem",
    drawer: false,
    searchfield: null,
    option: null,
    items: ["Title", "Author", "Year", "ISBN"],
    response: [],
    response_review: [],
    status: false,
    headers: [
      { text: "ISBN", value: "isbn" },
      { text: "Title", value: "title" },
      { text: "Author", value: "author" },
      { text: "Year", value: "year" }
    ],
    headers_book: [
      { text: "Username", value: "username" },
      { text: "Review", value: "review" },
      { text: "Rating", value: "rating" }
    ],
    selected_book: [
      { isbn: 1234 },
      { title: "default" },
      { year: 2020 },
      { author: "default" }
    ],
    goodread_reviews: null,
    rating: {
      avg_rating: 0.0,
      no_rating: "Unknown"
    },
    dialog: false,
    rev_dialog: false,
    user_review: "",
  }),
  methods: {
    logout() {
      eventBus.$emit("log-out", "login");
    },
    booksearch() {
      axios
        .get("http://127.0.0.1:5000/booksearch", {
          params: {
            book: this.searchfield,
            option: this.option
          },
          proxy: {
            host: "http://127.0.0.1",
            port: 5000
          }
        })
        .then(result => {
          this.response = null;
          this.response = result.data.result;
          if (!this.response.length) {
            // if book cannot be found, display error message
            this.message = "Your book is in another castle. Please try again.";
            this.status = true;
          } else {
            this.message = "Books Found!";
            this.status = true;
          }
        });
    },
    //
    handleClick(value) {
      this.selected_book = value;
      this.dialog = true;
      //get ratings from goodreads
      axios
        .get("http://127.0.0.1:5000/goodread", {
          params: {
            isbn: this.selected_book.isbn
          },
          proxy: {
            host: "http://127.0.0.1",
            port: 5000
          }
        })
        .then(result => {
          //checks to see if goodread api returns any books, if so store ratings and number of ratings
          this.goodread_reviews = result.data;
          if (this.goodread_reviews.status == "good") {
            this.rating.avg_rating = Number(
              this.goodread_reviews.goodread.books[0].average_rating
            );
            this.rating.no_rating = this.goodread_reviews.goodread.books[0].ratings_count;
          }
        });
      //get reviews from database
    },
    submit_review() {
      this.rev_dialog = true;
    },
    mounted() {
      eventBus.$on("pass-user", data => {
        this.user = data;
      });
    }
  },
  props: ["username"]
};
</script>

<style scoped>
.rounded-card {
  border-radius: 50px;
}

.register-box {
  width: 40%;
  padding-left: 5%;
  padding-top: 2%;
}
</style>