using System;
using System.Text;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Audio;
using Microsoft.Xna.Framework.Content;
using Microsoft.Xna.Framework.GamerServices;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using Microsoft.Xna.Framework.Media;

using Newtonsoft.Json;
using ZeroMQ;

namespace pocorn
{
    /// <summary>
    /// This is the main type for your game
    /// </summary>
    public class Game1 : Microsoft.Xna.Framework.Game
    {       
        GraphicsDeviceManager graphics;
        SpriteBatch spriteBatch;

        // Zmq specifics
        ZmqContext context; 
        ZmqSocket client;

        // Game specifics
        Pacman tipito;
        Int32 step = 20;

        Random rand = new Random();
        Texture2D pacmanTexture;
        Rectangle currentSquare;
        const float TimePerSquare = 0.75f;
        Color[] colors = new Color[3] { Color.Red, Color.Green,
           Color.Blue };

        public Game1()
        {
            graphics = new GraphicsDeviceManager(this);
            graphics.PreferredBackBufferHeight = 600;
            graphics.PreferredBackBufferWidth = 800;
            //graphics.IsFullScreen = true;
            Content.RootDirectory = "Content";

            this.TargetElapsedTime = TimeSpan.FromSeconds(1.0f / 5.0f);
            this.IsFixedTimeStep = false;
            this.step = this.graphics.PreferredBackBufferWidth / 15;
        }

        /// <summary>
        /// Allows the game to perform any initialization it needs to before starting to run.
        /// This is where it can query for any required services and load any non-graphic
        /// related content.  Calling base.Initialize will enumerate through any components
        /// and initialize them as well.
        /// </summary>
        protected override void Initialize()
        {
            // TODO: Add your initialization logic here

            base.Initialize();
            currentSquare = new Rectangle(
                rand.Next(0, this.Window.ClientBounds.Width - 25),
                rand.Next(0, this.Window.ClientBounds.Height - 25),
                24, 32);

            this.initializeChannel();
        }

        private void initializeChannel() 
        {
            this.context = ZmqContext.Create();
            this.client = this.context.CreateSocket(SocketType.PULL);

            this.client.Connect("tcp://10.0.0.22:3000");
            
        }

        /// <summary>
        /// LoadContent will be called once per game and is the place to load
        /// all of your content.
        /// </summary>
        protected override void LoadContent()
        {
            // Create a new SpriteBatch, which can be used to draw textures.
            spriteBatch = new SpriteBatch(GraphicsDevice);

            // TODO: use this.Content to load your game content here
            pacmanTexture = Content.Load<Texture2D>("pacman1");

            tipito = new Pacman(pacmanTexture);
        }

        /// <summary>
        /// UnloadContent will be called once per game and is the place to unload
        /// all content.
        /// </summary>
        protected override void UnloadContent()
        {
            // TODO: Unload any non ContentManager content here
        }

        /// <summary>
        /// Allows the game to run logic such as updating the world,
        /// checking for collisions, gathering input, and playing audio.
        /// </summary>
        /// <param name="gameTime">Provides a snapshot of timing values.</param>
        protected override void Update(GameTime gameTime)
        {
            // Allows the game to exit
            KeyboardState ks = Keyboard.GetState();
            if (ks.IsKeyDown(Keys.Escape))
            {
                this.client.Close();
                this.client.Dispose();
                this.context.Dispose();
            
                this.Exit();
            }
            

            // TODO: Add your update logic here

            base.Update(gameTime);

            processChannel();
            
        }

        private void processChannel()
        {
            Move reply = JsonConvert.DeserializeObject<Move>(client.Receive(Encoding.ASCII));

            processKeys(reply);
        }

        private void processKeys(Move m)
        {
            currentSquare.X -= m.left;
            currentSquare.X += m.right;
            currentSquare.Y -= m.front;
            currentSquare.Y += m.down;
        }

        /// <summary>
        /// This is called when the game should draw itself.
        /// </summary>
        /// <param name="gameTime">Provides a snapshot of timing values.</param>
        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(Color.Gray);

            // TODO: Add your drawing code here

            base.Draw(gameTime);

            spriteBatch.Begin();
            spriteBatch.Draw(
                pacmanTexture,
                currentSquare,
                colors[1]);
            spriteBatch.End();
        }
    }
}
