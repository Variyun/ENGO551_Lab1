<template>
  <v-app id="inspire">
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="elevation-12">
              <v-toolbar color="primary" dark flat>
                <v-toolbar-title>Login</v-toolbar-title>
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
                  />
                  <v-text-field
                    id="password"
                    label="Password"
                    v-model="user.password"
                    prepend-icon="mdi-lock"
                    type="password"
                  />
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-card-text>
                  Don't Have an Account?
                  <v-btn text @click="dialog = !dialog">Register Here</v-btn>
                </v-card-text>
                <v-spacer />
                <v-btn color="primary">Login</v-btn>
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
          <v-snackbar v-model="snackbar">
            <h3> Successfully Registered </h3>
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
                  id="password"
                  placeholder="abc123"
                  v-model="new_user.password"
                  type="password"
                  filled
                  required
                />
                <h2>Re-type Password</h2>
                <v-text-field
                  id="password"
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
  </v-app>
</template>
<script>
export default {
  name: "login",
  data() {
    return {
      overlay: false,
      dialog: false,
      register: false,
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
      snackbar: false
    };
  },
  methods: {
    validate() {
      if (this.new_user.password != this.new_user.re_password) {
        this.invalid = true;
      } else {
        this.invalid = false;
        this.dialog = false;
        this.snackbar = true;
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