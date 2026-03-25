import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createStytchUIClient, StytchProvider } from '@stytch/react';
import './index.css'
import App from './App.jsx'

const stytch = createStytchUIClient('public-token-test-8245b9fb-5d52-467a-8e75-ab2ce9defccf');

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <StytchProvider stytch={stytch}>
      <App />
    </StytchProvider>
  </StrictMode>,
)