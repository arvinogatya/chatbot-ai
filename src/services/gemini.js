import { GoogleGenAI } from '@google/genai'
const GEMINI_API = import.meta.env.VITE_GEMINI

const ai = new GoogleGenAI({ apiKey: GEMINI_API })

export const requestGemini = async (contents) => {
  const response = await ai.models.generateContent({
    model: 'gemini-2.0-flash',
    contents,
  })
  return response.text
}
