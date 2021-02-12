/**
 * Store
 *
 */
export const state = ()=>({
    started: null,
    locales: ['ja'],
    locale: 'ja',
    sessionId: null,
    lineUser: null,
    hairsalon: null,
    axiosError: null,
});

export const mutations = {
    clear(state) {
        state.started = null;
        state.locale = 'ja';
        state.sessionId = null;
        state.lineUser = null;
        state.hairsalon = null;
        state.axiosError = null;
    },
    started(state, started) {
        state.started = started;
    },
    locale(state, locale) {
        if (state.locales.includes(locale)) {
            state.locale = locale;
        }
    },
    session(state, sessionId) {
        state.sessionId = sessionId;
    },
    lineUser(state, lineUser) {
        state.lineUser = lineUser;
    },
    hairsalon(state, hairsalon) {
        state.hairsalon = hairsalon;
    },
    axiosError(state, axiosError) {
        state.axiosError = axiosError;
    },
};

export const getters = {
    axiosError(state) {
        return state.axiosError;
    },
    isAxiosError(state) {
        return state.axiosError != null ? true : false;
    }
}