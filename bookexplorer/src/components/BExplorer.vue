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
      <v-toolbar-title>BookExplorer</v-toolbar-title>
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
                <v-toolbar-title> {{ selected_book.title }}, ({{selected_book.isbn}}) </v-toolbar-title>
              </v-toolbar>
              <div class="register-box">
                <h3> Written by {{selected_book.author }}, {{selected_book.year}} </h3>
                <!-- goodreads api, get reviews and score --> 
                <v-btn color="indigo" dark> submit a review </v-btn>
              </div>
              <br/>
              <!-- display reviews -->
              <v-row align="center" justify="center">
                <v-data-table
                  :headers="headers_book"
                  :items="response_review"
                  :items-per-page="10"
                  class="elevation-1"
                  @click:row="handleClick"
                ></v-data-table>
              </v-row>
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
      { text: "Rating", value: "rating" },
    ],
    selected_book: [
      { isbn: 1234 },
      { title: "default" },
      { year: 2020 },
      { author: "default" },
    ],
    goodread_reviews: null,
    dialog: false,
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
      //https://www.goodreads.com/book/review_counts.json
      axios
        .get("https://www.goodreads.com/book/review_counts", {
          params: {
            key: "swIxMzw2BAh2FK5fXd3PSg",
            isbns: this.selected_book.isbn,
            format: "json"
          },
        })
        .then(result => {
          //if the username already exists, display error
          this.response_review = result;
        });
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
  width: 30%;
  padding-left: 5%;
  padding-top: 2%;
}
</style>