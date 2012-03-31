using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace pocorn
{
    class Pacman
    {
        public const int width = 13;
        public const int height = 13;

        private int spritesLeftIndex = 0;
        private int spritesRightIndex = 1;
        private int spritesUpIndex = 2;
        private int spritesDowntIndex = 3;


        private Texture2D pacmanTexture;

        public Pacman(Texture2D pacmanTexture)
        {
            this.pacmanTexture = pacmanTexture;
        }
 
        public void getCurrentTexture(KeyboardState currentKBState)
        {
            return ;
        }

    }
}
