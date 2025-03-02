import { TpaServer, TpaSession } from '@augmentos/sdk';

import * as fs from 'fs';
import * as path from 'path';

class ExampleAugmentOSApp extends TpaServer {
  private imageBase64: string;
  private image_index: number;
  private bitmapInterval: NodeJS.Timeout;

  constructor(config: any) {
    super(config);
    // start off with image 0

    this.image_index = 0;
    this.updateImage(this.image_index);
  }

  private updateImage(index: number) {
    try {
      if (index > 6571) { // bad apple specific
        index = 1;
      }
      const imagePath = path.join(__dirname, `final/${index}.bmp`);
      const imageBuffer = fs.readFileSync(imagePath);
      this.imageBase64 = imageBuffer.toString('base64');
      console.log(`Image updated to index ${index}`);
    } catch (error) {
      console.error(`Error reading or encoding image ${index}:`, error);
      this.imageBase64 = '';
    }
  }

  protected async onSession(session: TpaSession, sessionId: string, userId: string): Promise<void> {
    // loop sending images
    setInterval(() => {
      this.image_index += 1;
      this.updateImage(this.image_index);
      this.sendBitmap(session);
    }, 8000);

    // Unused other event handlers
    const cleanup = [
      session.events.onButtonPress((data) => {}), 
      
      session.events.onTranscription((data) => {}),

      session.events.onPhoneNotifications((data) => {}),

      session.events.onGlassesBattery((data) => {}),

      session.events.onError((error) => {
        console.error('Error:', error);
      })
    ];

    // Add cleanup handlers
    cleanup.forEach(handler => this.addCleanupHandler(handler));
  }

  private sendBitmap(session: TpaSession) {
    session.layouts.showBitmapView(this.imageBase64);
    console.log(`Sending bitmap image ${this.image_index} to glasses`);
  }
}

// Start the server
// DEV CONSOLE URL: https://augmentos.dev/
// Get your webhook URL from ngrok (or whatever public URL you have)
const app = new ExampleAugmentOSApp({
  packageName: 'org.kevin.badapple', // make sure this matches your app in dev console
  apiKey: 'your_api_key', // Not used right now, can be anything
  port: 80, // The port you're hosting the server on
  augmentOSWebsocketUrl: 'wss://dev.augmentos.org/tpa-ws' //AugmentOS url
});

app.start().catch(console.error);