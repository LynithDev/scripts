#!/usr/bin/env bash
INTERFACE="/org/gnome/desktop/interface"

change_theme() {
    THEME="$(dconf read $INTERFACE/color-scheme)"
    if [[ $THEME == "'prefer-dark'" ]]; then
        # GTK+ Theme
        gsettings set org.gnome.desktop.interface gtk-theme 'adw-gtk3-dark'
     
        # Restart Discord
        #if pgrep -f "/opt/discord/Discord" >/dev/null 2>&1; then
         #   pkill discord && discord
        #fi

        # Alacritty theme
        sed -i 's+- ~/.config/alacritty/colors-light.yml+- ~/.config/alacritty/colors-dark.yml+g' ~/.config/alacritty/alacritty.yml
    else
        # GTK+ Theme
        gsettings set org.gnome.desktop.interface gtk-theme 'adw-gtk3'
        
        # Restart Discord
        # if pgrep -f "/opt/discord/Discord" >/dev/null 2>&1; then
          #  pkill discord
        #fi

        # Alacritty theme
        sed -i 's+- ~/.config/alacritty/colors-dark.yml+- ~/.config/alacritty/colors-light.yml+g' ~/.config/alacritty/alacritty.yml
    fi
}

while read -r line; do
    [[ -n $line ]] || change_theme 
done < <(dconf watch /org/gnome/desktop/interface/color-scheme)


