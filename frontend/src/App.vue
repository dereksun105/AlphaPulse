<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <header>
      <h1>AlphaPulse Dashboard</h1>
    </header>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style>
body {
  margin: 0;
  background-color: #000;
  font-family: 'Inter', sans-serif;
}

.app-container {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 20px;
  box-sizing: border-box;
}

header {
  margin-bottom: 30px;
  border-bottom: 1px solid #333;
  padding-bottom: 20px;
}

h1 {
  color: #fff;
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(to right, #4caf50, #2196f3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
