

 <template>
  <header>
    <h1>Database Configuration</h1>
  </header>
  <form @submit.prevent="startProcess" class="form-container">
    <div class="form-group">
      <input type="text" id="tele" v-model="tele" placeholder="手机号" required>
      <button type="submit" class="btn-submit">Start Process</button>
    </div>
  </form>
  <div class="container">
    <div id="messages" class="messages-container">
      <h2>Output:</h2>
      <pre>{{ messages }}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tele: '',
      messages: ''
    };
  },
  methods: {
    async startProcess() {
      const params = {
        tele: this.tele,
      };
      try {
        await axios.post('http://localhost:5174/execute', params);
        
        const eventSource = new EventSource('http://localhost:5174/stream');
        eventSource.onmessage = (event) => {
          this.messages += event.data + '\n';
        };

        eventSource.onerror = (error) => {
          console.error('EventSource failed:', error);
          eventSource.close();
        };
      } catch (error) {
        console.error('Error starting process:', error);
      }
    }
  }
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items:  flex-start;
  height: 100vh;
  box-sizing: border-box;
}

.container {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 900px;
  text-align: left;
  margin-top: 20px;
}

header {
  margin-bottom: 10px;
  text-align: left;
  width: 600px;
}

h1 {
  font-size: 24px;
  color: #333;
  margin: 100;
}

.form-container {
  margin-bottom: 0;
  width: 600px;
}
.form-group {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

input {
  width: 60%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px 0 0 4px;
  outline: none;
}

.btn-submit {
  padding: 10px 20px;
  border: 1px solid #007bff;
  border-radius: 0 4px 4px 0;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  outline: none;
}

.btn-submit:hover {
  background-color: #0056b3;
}

.messages-container {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #ddd;
  text-align: left;
}

h2 {
  font-size: 20px;
  margin-bottom: 10px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
}
</style>