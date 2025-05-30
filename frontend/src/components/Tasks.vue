<script setup>
import Loader from './Loader.vue'
import { onMounted, ref } from 'vue'
import { useToast } from 'vue-toastification';
import axios from 'axios'

const tasks = ref([])
const newTitle = ref('')

const showLoader = ref(false)
const errorMessage = ref(null)
const showError = ref(false)

const editingTaskId = ref(null)
const editedTitle = ref('')


const toast = useToast();


const startEditing = (task) => {
  editingTaskId.value = task.id
  editedTitle.value = task.title
}

const cancelEditing = () => {
  editingTaskId.value = null
  editedTitle.value = ''
}

const saveEdit = async (task) => {
  const newTitle = editedTitle.value.trim()
  if (!newTitle || newTitle === task.title) {
    cancelEditing()
    return
  }

  showLoader.value = true
  try {
    const response = await axios.patch(`/api/v1/tasks/${task.id}/`, {
      title: newTitle,
    })
    task.title = response.data.title
    cancelEditing()
  } catch (error) {
    errorMessage.value = "Ошибка при редактировании задачи!"
    showError.value = true
  } finally {
    showLoader.value = false
  }
}


const fetchTasks = async () => {
  showLoader.value = true
  try {
    const response = await axios.get('/api/v1/tasks/')
    tasks.value = response.data
    showLoader.value = false
  } catch (error) {
    errorMessage.value = "Ошибка получения задач!"
    showError.value = true
  }
}

const addTask = async () => {
  const title = newTitle.value.trim()
  if (!title) return

  showLoader.value = true
  try {
    const response = await axios.post('/api/v1/tasks/', {
      title,
      completed: false,
    })
    tasks.value.unshift(response.data)
    newTitle.value = ''
    toast.success(`Task ${title} Added`);
  } catch (error) {
    errorMessage.value = "Ошибка при добавлении задачи!"
    showError.value = true
  } finally {
    showLoader.value = false
  }
}

const deleteTask = async (id) => {
  showLoader.value = true
  try {
    await axios.delete(`/api/v1/tasks/${id}/`)
    tasks.value = tasks.value.filter(task => task.id !== id)
  } catch (error) {
    errorMessage.value = "Ошибка при удалении задачи!"
    showError.value = true
  } finally {
    showLoader.value = false
  }
}

const toggleCompleted = async (task) => {
  showLoader.value = true
  try {
    const response = await axios.patch(`/api/v1/tasks/${task.id}/`, {
      completed: !task.completed,
    })
    task.completed = response.data.completed
  } catch (error) {
    errorMessage.value = "Ошибка при обновлении статуса!"
    showError.value = true
  } finally {
    showLoader.value = false
  }
}

onMounted(fetchTasks)
</script>

<template>
  <transition name="fade">
    <div v-if="showError" class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-4">
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden max-w-md w-full mx-auto">
        <!-- Header -->
        <div class="bg-red-600 px-6 py-4 flex items-center">
          <!-- Иконка 💥 можно заменить на SVG из heroicons -->
          <span class="text-2xl mr-3">⚠️</span>
          <h2 class="text-lg font-semibold text-white flex-1">
            Ошибка
          </h2>
          <button @click="showError = false" class="text-white hover:text-red-200" aria-label="Закрыть">
            ✕
          </button>
        </div>
        <!-- Body -->
        <div class="px-6 py-4">
          <p class="text-gray-700 text-center">
            {{ errorMessage }}
          </p>
        </div>
        <!-- Footer -->
        <div class="px-6 py-4 bg-gray-50 flex justify-end">
          <button @click="showError = false"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition">
            Ок
          </button>
        </div>
      </div>
    </div>
  </transition>

  <div class="min-h-screen flex items-center justify-center bg-indigo-300">
    <Loader v-if="showLoader == true" />
    <div v-if="showLoader == false" class="rounded-3xl p-4 max-w-xl w-full bg-white shadow fade-in">

      <div class="p-4 max-w-xl w-full bg-white">
        <h1 class="text-2xl font-bold mb-4 text-center">Task List</h1>


        <div class="flex flex-col sm:flex-row mb-4 gap-2">
          <input v-model="newTitle" type="text" placeholder="New Task" class="flex-1 p-2 border rounded-2xl px-4" />
          <button @click="addTask"
            class="w-full sm:w-auto px-6 py-2 bg-pink-500 text-white rounded-3xl hover:bg-pink-600">Add</button>
        </div>

        <ul class="space-y-2 overflow-y-auto max-h-[50vh]">
          <li v-for="task in tasks" :key="task.id" class="p-2 border rounded flex flex-col sm:flex-row">
            <div class="flex-1">
              <div v-if="editingTaskId === task.id" class="flex gap-2 items-center">
                <input v-model="editedTitle" class="flex-1 p-1 border rounded" />
                <button @click="saveEdit(task)"
                  class="px-2 py-1 bg-green-500 text-white  hover:bg-green-600 rounded-3xl">Save</button>
                <button @click="cancelEditing"
                  class="px-2 py-1 bg-gray-400 text-white  hover:bg-gray-500 rounded-3xl">Cancel</button>
              </div>
              <div v-if="editingTaskId !== task.id" class="flex gap-2">
                <input type="checkbox" :checked="task.completed" @change="toggleCompleted(task)"
                  class="w-6 h-6 accent-green-600 rounded-3xl border-gray-300 focus:ring-2 focus:ring-green-400" />
                <span :class="{ 'line-through text-gray-500': task.completed }" class="font-medium">{{ task.title
                  }}</span>
              </div>
            </div>
            <div v-if="editingTaskId !== task.id" class="flex gap-2">
              <button @click="startEditing(task)"
                class="px-2 py-1 bg-lime-500 text-white rounded-3xl hover:bg-lime-600">Edit Title</button>
              <button @click="deleteTask(task.id)"
                class="px-2 py-1 bg-purple-500 text-white rounded-3xl hover:bg-purple-600">Delete</button>
            </div>
          </li>

        </ul>
      </div>
    </div>
  </div>
</template>


<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}

.fade-in {
  animation: fadeIn 0.3s ease-out;
}


/* Простая анимация появления через Vue transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
