<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" app>
      <v-list dense>
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-contact-mail</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Account</v-list-item-title>
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
    <!-- content of the website -->
    <v-content>
      <v-container class="fill-height" fluid>
        <!-- Search bar -->
        <v-row style="height: 400px;">

          <v-col class="d-flex" >
              <v-text-field placeholder="Search..." type="text" v-model="searchfield"/> 
          </v-col>

          <v-col class="d-flex">
            <v-select :items="items" placeholder="Pick One" v-model="option"></v-select>
          </v-col>

          <v-col class="d-flex">
            <v-btn @click="booksearch">
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </v-col>

        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import axios from 'axios'
import { eventBus } from "../main.js";
export default {
  name: "BExplorer",
  data: () => ({
    drawer: false,
    user: null,
    searchfield: null,
    option: null,
    items: ['Title', 'Author', 'Year', 'ISBN'],
    response: [],
  }),
  methods: {
    logininfo(username) {
      this.user = username;
    },
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
            //if the username already exists, display error
            this.response = result;
          });
    }
  }
};
</script>

<style scoped>
.rounded-card {
  border-radius: 50px;
}
</style>