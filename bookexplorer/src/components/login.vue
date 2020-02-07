<template>
  <v-app id="inspire">
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="elevation-12">
              <v-toolbar color="primary" dark flat>
                <v-toolbar-title>Login to BookExplorer</v-toolbar-title>
                <v-spacer />
                <v-tooltip right>
                  <template v-slot:activator="{ on }">
                    <v-btn icon large target="_blank" v-on="on" @click="overlay = !overlay">
                      <v-icon>mdi-help-circle</v-icon>
                    </v-btn>
                  </template>
                  <span>About</span>
                </v-tooltip>
                <!-- Let the user know what to do -->
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    label="Username"
                    v-model="user.username"
                    prepend-icon="mdi-face-profile"
                    type="text"
                    @keyup.enter="logging"
                  />
                  <v-text-field
                    label="Password"
                    v-model="user.password"
                    prepend-icon="mdi-lock"
                    type="password"
                    @keyup.enter="logging"
                  />
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-card-text>
                  Don't Have an Account?
                  <v-btn text @click="dialog = !dialog">Register Here</v-btn>
                </v-card-text>
                <v-spacer />
                <v-btn color="primary" @click="logging">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
      <!-- about message -->
      <div class="text-center">
        <v-overlay :value="overlay">
          <v-card light>
            <v-card-text>
              <h1>Welcome to BookExplorer!</h1>
              <br />
              <h3>BookExplorer is an app that lets you look up any book by title, author, and even ISBN!</h3>
              <h3>With BookExplorer, you can even look at reviews and submit your own as well.</h3>
              <br />
              <h2>To start, please log in!</h2>
            </v-card-text>
          </v-card>
          <v-btn icon @click="overlay = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-overlay>
      </div>
      <!-- Message if user is able to register -->
      <template>
        <div class="text-center ma-2">
          <v-snackbar top v-model="snackbar">
            <h3>Successfully Registered</h3>
            <v-btn color="pink" text @click="snackbar = false">Close</v-btn>
          </v-snackbar>
        </div>
      </template>
    </v-content>
    <!-- register user -->
    <template>
      <v-row justify="center">
        <v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
          <v-card>
            <v-toolbar dark color="primary">
              <v-btn icon dark @click="dialog = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <v-toolbar-title>Please Enter in Your Information</v-toolbar-title>
            </v-toolbar>
            <v-alert
              dark
              type="error"
              v-model="invalid"
              transition="scale-transition"
            >Passwords do not match!</v-alert>
            <v-alert
              dark
              type="error"
              v-model="names"
              transition="scale-transition"
            >Username already exists!</v-alert>
            <div class="register-box">
              <v-form>
                <h2>Username</h2>
                <v-text-field
                  placeholder="root"
                  v-model="new_user.username"
                  type="text"
                  filled
                  required
                />
                <h2>Password</h2>
                <v-text-field
                  placeholder="abc123"
                  v-model="new_user.password"
                  type="password"
                  filled
                  required
                />
                <h2>Re-type Password</h2>
                <v-text-field
                  placeholder="abc123"
                  v-model="new_user.re_password"
                  type="password"
                  filled
                  required
                />
                <v-btn dark color="blue" class="mr-4" @click="validate">submit</v-btn>
              </v-form>
            </div>
          </v-card>
        </v-dialog>
      </v-row>
    </template>
    <!-- Message if user is able to register -->
    <template>
      <div class="text-center ma-2">
        <v-snackbar top v-model="failed">
          <h3>Registration failed, please check your credentials and try again later</h3>
          <v-btn color="pink" text @click="failed = false">Close</v-btn>
        </v-snackbar>
      </div>
    </template>
        <template>
      <div class="text-center ma-2">
        <v-snackbar top v-model="logerror">
          <h3>Could not log in. Please check your username and password!</h3>
          <v-btn color="pink" text @click="logerror = false">Close</v-btn>
        </v-snackbar>
      </div>
    </template>
  </v-app>
</template>

<script>
import axios from "axios";
import {eventBus} from "../main.js";

export default {
  name: "login",
  data() {
    return {
      overlay: false,
      dialog: false,
      register: false,
      names: false,
      user: {
        username: null,
        password: null
      },
      new_user: {
        username: null,
        password: null,
        re_password: null
      },
      invalid: false,
      snackbar: false,
      failed: false,
      logerror: false,
      loggedin: false,
      response: true,
      response2: null
    };
  },

  methods: {
    // function to vallidate registration
    validate() {
      if (this.new_user.password != this.new_user.re_password) {
        this.invalid = true;
        //if password matches then submit to database
      } else {
        this.invalid = false;
        //if passwords match, check to see if username already exists
        axios
          .get("http://127.0.0.1:5000/namecheck", {
            params: {
              username: this.new_user.username
            },
            proxy: {
              host: "http://127.0.0.1",
              port: 5000
            }
          })
          .then(result => {
            //if the username already exists, display error
            this.response2 = result;
            if (result.data.exists == "true") {
              this.names = true;
            } else {
              this.dialog = false;
              this.registering();
            }
          });
      }
    },
    //function to register user - send http request to back
    registering() {
      axios
        .get("http://127.0.0.1:5000/register", {
          params: {
            username: this.new_user.username,
            password: this.new_user.password
          },
          proxy: {
            host: "http://127.0.0.1",
            port: 5000
          }
        })
        .then(result => {
          this.response = result;
          this.worked();
        });
    },
    //function to log in user 
    logging() {
      axios
        .get("http://127.0.0.1:5000/loggingin", {
          params: {
            username: this.user.username,
            password: this.user.password
          },
          proxy: {
            host: "http://127.0.0.1",
            port: 5000
          }
        })
        .then(result => {
          //if the username already exists, display error
          this.response2 = result;
          if (result.data.loggedin == "true") {
            this.loggedin = true;
            //send username to application 
            eventBus.$emit("log-in", {tab: "BExplorer", user: this.user.username});
            this.user.username = null;
            this.user.password = null;
          } else {
            this.logerror = true;
          }
        });
    },
    worked() {
      if (this.response.data == "failed") {
        this.failed = true;
      } else {
        this.snackbar = true;
        //reset registration fields
        this.new_user.username = null;
        this.new_user.password = null;
        this.new_user.re_password = null;
      }
    }
  }
};
</script>

<style>
.register-box {
  width: 30%;
  padding-left: 5%;
  padding-top: 2%;
}
</style>