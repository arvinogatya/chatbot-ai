<script setup>
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import { useSlots, ref, defineEmits, onMounted } from 'vue'
import IconCopy from './icons/IconCopy.vue'
import IconCheck from './icons/IconCheck.vue'

const slots = useSlots()
const emit = defineEmits(['doneTyping'])

const rawText = ref(slots.default?.()[0]?.children || '')
const htmlContent = ref('')
const output = ref('')
const isCopy = ref(false)
const isDone = ref(false)

// Set up marked with highlighting
marked.setOptions({
  highlight(code, lang) {
    if (hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  },
  langPrefix: 'hljs language-',
})

onMounted(() => {
  const chars = rawText.value.split('')
  chars.forEach((char, index) => {
    setTimeout(() => {
      output.value += char
      htmlContent.value = marked(output.value)
      if (index === chars.length - 1) {
        isDone.value = true
        emit('doneTyping') //  Emit to parent when finished
      }
    }, index * 5)
  })
})

// Copy button
const copy = () => {
  isCopy.value = true
  navigator.clipboard.writeText(rawText.value)
  setTimeout(() => {
    isCopy.value = false
  }, 1000)
}
</script>

<template>
  <div class="w-full flex justify-start h-fit mb-2 flex-col gap-2">
    <div
      class="mr-2 w-fit text-stone-900 dark:bg-grey-200 bg-gray-200 p-4 rounded-r-xl rounded-tl-xl border border-black overflow-x-hidden whitespace-normal max-w-full"
      v-html="htmlContent"
    ></div>
    <!-- <button @click="copy" class="flex justify-start" v-if="!isCopy && isDone">
      <IconCopy /> Copy
    </button>
    <button @click="copy" class="flex justify-start" v-if="isCopy && isDone" disabled>
      <IconCheck /> Copied
    </button> -->
  </div>
</template>

<style scope>
pre {
  background: rgb(29, 29, 29);
  color: white;
  overflow: auto;
  padding: 8px;
  border-radius: 6px;
  border: gray solid 1px;
  margin: 2em 0px;
}
code {
  font-family: monospace;
  margin: 2px;
  font-size: 1.2em;
}

ol,
ul {
  list-style: disc;
  margin: 1em;
}
ol {
  list-style: decimal;
}
</style>
