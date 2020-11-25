const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  purge: [
    '../templates/**/*.html',
    '../../templates/**/*.html',
  ],
  theme: {
    extend: {
      backgroundOpacity: {
        20: "0.2",
        35: "0.35",
      },
      fontFamily: {
        sans: ["Roboto", ...defaultTheme.fontFamily.sans],
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
