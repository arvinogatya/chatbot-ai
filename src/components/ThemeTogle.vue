<script setup>
import IconDark from './icons/IconDark.vue'
import IconLight from './icons/IconLight.vue'
import { ref } from 'vue'

// Atur default tema jika belum ada
if (!localStorage.getItem('theme')) {
  localStorage.setItem('theme', 'light')
}

// Ambil tema dari localStorage
const theme = ref(localStorage.getItem('theme'))

// Terapkan kelas tema saat halaman dimuat
if (theme.value === 'dark') {
  document.documentElement.classList.add('dark')
} else {
  document.documentElement.classList.remove('dark')
}

// Fungsi untuk mengganti tema
const changeTheme = () => {
  if (theme.value === 'dark') {
    theme.value = 'light'
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  } else {
    theme.value = 'dark'
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  }
}
</script>

<template>
  <div class="absolute left-5">
    <button @click="changeTheme" v-if="theme == 'dark'">
      <IconLight />
    </button>
    <button @click="changeTheme" v-if="theme != 'dark'">
      <IconDark />
    </button>
  </div>
</template>
