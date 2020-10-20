const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
    // defaultLineHeights: true,
    // standardFontWeights: true
  },
  purge: [
    // Templates within theme app (e.g. base.html)
    '../templates/**/*.html',
    // Templates in other apps
    '../../templates/**/*.html',
  ],
  theme: {
    extend: {
      backgroundOpacity: {
        20: "0.2",
      },
      fontFamily: {
        sans: ["Roboto", ...defaultTheme.fontFamily.sans],
      },
      padding: {},
      fontSize: {
        "2sm": "0.875rem",
        "2lg": "1.25rem",
      },
      boxShadow: {
        button: "0 3px 12px 0 rgba(0, 0, 0, 0.06)",
      },
      colors: {
        "primary-blue": "#2FACDB",
      },
    },
  },
  // to enable group-hover
  variants: {
    textColor: ["responsive", "hover", "focus", "group-hover"],
    textOpacity: ["responsive", "hover", "focus", "group-hover"],
  },
  plugins: [require("@tailwindcss/ui")],
};
