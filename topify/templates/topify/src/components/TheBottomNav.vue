<template>
  <v-bottom-nav :value="true" fixed app>
    <v-btn color="teal" flat value="process" to="/process">
      <span>Process</span>
      <v-icon>mdi-file-tree</v-icon>
    </v-btn>
    <v-btn color="teal" flat value="docker" to="/docker">
      <span>Docker</span>
      <v-icon>mdi-docker</v-icon>
    </v-btn>
  </v-bottom-nav>
</template>
