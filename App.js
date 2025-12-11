import logo from './logo.svg';
import './App.css';
import AppRouter from './Router';
import { ToastContainer, toast } from 'react-toastify';

function App() {
  return (
    <div>
      <AppRouter/>
      <ToastContainer/>
    </div>
  );
}

export default App;
