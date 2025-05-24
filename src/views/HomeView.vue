<script setup>
import UserChat from '../components/UserChat.vue'
import BotChat from '../components/BotChat.vue'
// import ThemeTogle from '../components/ThemeTogle.vue'
import { requestGemini } from '@/services/gemini'
import { greetingTime } from '@/services/greeting'
import { ref, nextTick, onMounted } from 'vue'
import IconLoad from '../components/icons/IconLoad.vue'

const input = ref('')
const isLoading = ref(false)
const greeting = ref('')
onMounted(() => {
  greeting.value = greetingTime()
})

const userChats = ref([])
const botChats = ref([])
const chatContainer = ref(null)

const handleAsk = async () => {
  // show bubble chat
  if (input.value.trim() === '') return

  const userChat = input.value.trim()

  userChats.value.push(input.value)
  input.value = ''
  await scrollToBottom()
  isLoading.value = true

  // request to gemini
  try {
    const botReply = await requestGemini(userChat)
    botChats.value.push(botReply)
  } catch (error) {
    const errMsg = 'Error while processing request'
    botChats.value.push(errMsg)
    console.error('Gemini ora mundeng laeekk', error)
  }
  isLoading.value = false
}

// scroll to bottom
const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTo({
      top: chatContainer.value.scrollHeight,
      behavior: 'smooth',
    })
  }
}
</script>
<template>
  <div class="blackbox-container">
    <header class="header items-start">
      <!-- <ThemeTogle /> -->
      <h2 class="title">TEKON OPO AE LAEEKK</h2>
    </header>

    <main
      ref="chatContainer"
      class="chat-area"
      @scroll.passive="onScroll"
      role="log"
      aria-live="polite"
    >
      <div v-if="userChats.length === 0" class="empty-state">
        <p>ada yang bisa saya bantuuu??</p>
      </div>

      <div class="messages" role="list">
        <div
          v-for="(msg, idx) in userChats"
          :key="idx"
          class="message-pair"
          role="listitem"
        >
          <UserChat class="user-message">{{ msg }}</UserChat>
          <BotChat
            v-if="botChats[idx]"
            @doneTyping="scrollToBottom"
            class="bot-message"
          >
            {{ botChats[idx] }}
          </BotChat>
        </div>
      </div>
    </main>

    <footer class="input-footer" role="form" aria-label="Message input form">
      <textarea
        v-model="input"
        placeholder="Type your message..."
        class="input-field"
        rows="1"
        @keydown.enter.exact.prevent="handleAsk"
        aria-label="Chat input"
      ></textarea>
      <button
        v-if="!isLoading && input.trim() !== ''"
        @click="handleAsk"
        class="btn-send"
        aria-label="Send message"
      >
        Send
      </button>
      <button v-else class="btn-send loading" disabled aria-label="Loading">
        <IconLoad class="spinner" />
      </button>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'BlackboxChat',
  components: {
    ThemeTogle: {},
    UserChat: {},
    BotChat: {},
    IconLoad: {},
  },
  data() {
    return {
      input: '',
      userChats: [],
      botChats: [],
      isLoading: false,
      autoScrollEnabled: true,
    };
  },
  methods: {
    async handleAsk() {
      if (!this.input.trim()) return;
      this.isLoading = true;
      this.userChats.push(this.input.trim());
      this.input = '';
      this.botChats.push('');
      try {
        const response = await new Promise((resolve) =>
          setTimeout(() => resolve('This is a Blackbox AI style reply.'), 1600)
        );
        this.$set(this.botChats, this.botChats.length - 1, response);
      } catch {
        this.$set(this.botChats, this.botChats.length - 1, 'Error: Something went wrong.');
      } finally {
        this.isLoading = false;
        this.$nextTick(() => this.scrollToBottom());
      }
    },
    scrollToBottom() {
      const container = this.$refs.chatContainer;
      if (!container) return;
      container.scrollTop = container.scrollHeight;
    },
    onScroll() {
      const container = this.$refs.chatContainer;
      this.autoScrollEnabled =
        container.scrollTop + container.clientHeight >= container.scrollHeight - 15;
    },
  },
  watch: {
    botChats() {
      if (this.autoScrollEnabled) {
        this.$nextTick(() => this.scrollToBottom());
      }
    },
  },
  mounted() {
    this.scrollToBottom();
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.blackbox-container {
  font-family: 'Inter', sans-serif;
  background-color: #121217;
  color: #e5e5e5;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 0 5rem;
}

.header {
  width: 90vw;
  max-width: 720px;
  padding: 1rem 1.5rem;
  margin: 1rem auto 0;
  background-color: #1f2029;
  border-radius: 0.75rem;
  box-shadow: 0 4px 14px rgb(10 10 10 / 0.5);
  color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  user-select: none;
}

.title {
  font-weight: 600;
  font-size: 1.6rem;
  user-select: none;
  letter-spacing: 0.02em;
}

/* Chat Area */
.chat-area {
  width: 90vw;
  max-width: 720px;
  background-color: #1e1e2f;
  border-radius: 1rem;
  height: 78vh;
  margin: 1rem auto 0;
  padding: 1.5rem 2rem;
  box-shadow: inset 0 0 12px #111;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
  scroll-behavior: smooth;
  position: relative;
  color: #ddd;
}

.empty-state {
  font-size: 1.4rem;
  color: #7f7f9a;
  text-align: center;
  margin-top: 4rem;
  user-select: none;
}

/* Messages */
.messages {
  display: flex;
  flex-direction: column;
  gap: 1.3rem;
}

.message-pair {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

/* User Chat bubble */
UserChat {
  align-self: flex-end;
  background: #7c5dfa;
  color: white;
  padding: 0.85rem 1.3rem;
  border-radius: 20px 20px 0 20px;
  max-width: 75%;
  white-space: pre-wrap;
  box-shadow: 0 6px 12px rgb(124 93 250 / 0.5);
  font-size: 1rem;
  user-select: text;
}

/* Bot Chat bubble */
BotChat {
  align-self: flex-start;
  background: #2d2f49;
  color: #ccccee;
  padding: 0.85rem 1.3rem;
  border-radius: 20px 20px 20px 0;
  max-width: 75%;
  white-space: pre-wrap;
  box-shadow: 0 6px 14px rgb(45 47 73 / 0.6);
  font-size: 1rem;
  font-family: 'Source Code Pro', monospace;
  user-select: text;
}

/* Input footer */
.input-footer {
  position: fixed;
  bottom: 1.25rem;
  width: 90vw;
  max-width: 720px;
  background-color: #1f2029;
  border-radius: 2rem;
  padding: 0.85rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 10px 18px rgb(124 93 250 / 0.7);
  border: 1px solid #7c5dfa;
  z-index: 150;
}

/* Textarea */
.input-field {
  flex-grow: 1;
  background-color: #1a1a2f;
  border: none;
  border-radius: 1.5rem;
  padding: 0.7rem 1rem;
  font-size: 1rem;
  color: #e5e5e5;
  font-family: 'Inter', sans-serif;
  outline: none;
  resize: none;
  box-shadow: inset 0 0 10px #5e4fd1;
  transition: background-color 0.25s ease;
  min-height: 40px;
}

.input-field::placeholder {
  color: #8888aa;
  font-style: italic;
}

.input-field:focus {
  background-color: #271f5a;
  box-shadow: 0 0 10px #7c5dfa;
}

/* Buttons */
.btn-send {
  background-color: #7c5dfa;
  color: white;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  padding: 0.5rem 1.8rem;
  border-radius: 1.5rem;
  cursor: pointer;
  user-select: none;
  box-shadow: 0 6px 14px rgb(124 93 250 / 0.8);
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
}

.btn-send:hover:not(:disabled) {
  background-color: #906dff;
  box-shadow: 0 8px 18px rgb(144 109 255 / 0.9);
}

.btn-send:disabled {
  opacity: 0.55;
  cursor: default;
  box-shadow: none;
}

.spinner {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  color: white;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

/* Scrollbar styling */
.chat-area::-webkit-scrollbar {
  width: 8px;
}

.chat-area::-webkit-scrollbar-track {
  background: #1e1e2f;
}

.chat-area::-webkit-scrollbar-thumb {
  background-color: #7c5dfa;
  border-radius: 10px;
  border: 2px solid #1e1e2f;
}

/* Responsive */
@media (max-width: 480px) {
  .header {
    font-size: 1.4rem;
  }

  UserChat,
  BotChat {
    max-width: 90%;
  }

  .input-footer {
    padding: 0.7rem 1rem;
    gap: 0.65rem;
  }

  .btn-send {
    padding: 0.5rem 1.3rem;
    height: 36px;
  }
}
</style>

