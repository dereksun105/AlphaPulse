<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <header>
      <div class="logo">
        <h1>AlphaPulse</h1>
        <span class="beta-tag">BETA</span>
      </div>
      <nav>
        <RouterLink to="/">儀表板 (Dashboard)</RouterLink>
        <RouterLink to="/techniques">技術詳解 (Techniques)</RouterLink>
        <RouterLink to="/models">模型日誌 (Model Diary)</RouterLink>
      </nav>
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
  color: #fff;
}

.app-container {
  width: 100%;
  min-height: 100vh;
  margin: 0;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  border-bottom: 1px solid #222;
  background: rgba(0,0,0,0.8);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

h1 {
  font-size: 1.5rem;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(to right, #2962FF, #2979FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.beta-tag {
  background: #2b2b2b;
  color: #888;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: bold;
}

nav {
  display: flex;
  gap: 30px;
}

nav a {
  color: #888;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
  font-size: 0.95rem;
}

nav a:hover, nav a.router-link-active {
  color: #fff;
}

nav a.router-link-active {
  color: #2962FF;
}

main {
  padding: 20px;
}
</style>
