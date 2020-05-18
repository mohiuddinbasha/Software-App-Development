import React from 'react';
import {View, Button, Text, ScrollView, StyleSheet, Switch, TextInput} from 'react-native'
import Constants from 'expo-constants'

let id = 0

const styles = StyleSheet.create({
  todoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingTop:10,
  },
  appContainer: {
    paddingTop: Constants.statusBarHeight,
  },
  fill: {
    flex: 1,
  }
})

const Todo = props => (
  <View style={styles.todoContainer}>
    <Switch value={props.todo.checked} onValueChange={props.onToggle} onTintColor="black" />
    <Button onPress={props.onDelete} title="delete" color="black" />
    <Text style={{paddingLeft:10}}>{props.todo.text}</Text>
  </View>
)

export default class App extends React.Component {
  constructor() {
    super()
    this.state = {
      todos: [],
      text: '',
    }
  }

  addTodo(text) {
    id++
    this.setState({
      todos: [
        ...this.state.todos,
        {id: id, text: text, checked: false},
      ],
      text: '',
    })
  }

  takeInput = (input) => {
      this.setState({ text: input })
  }

  removeTodo(id) {
    this.setState({
      todos: this.state.todos.filter(todo => todo.id !== id)
    })
  }

  toggleTodo(id) {
    this.setState({
      todos: this.state.todos.map(todo => {
        if (todo.id !== id) return todo
        return {
          id: todo.id,
          text: todo.text,
          checked: !todo.checked,
        }
      })
    })
  }

  render() {
    return (
      <View style={[styles.appContainer, styles.fill]}>
        <Text>Todo count: {this.state.todos.length}</Text>
        <Text>Unchecked todo count: {this.state.todos.filter(todo => !todo.checked).length}</Text>
        <TextInput
          style={{ height: 40, borderWidth: 2, margin: 10, borderColor: 'gray', paddingLeft:10}}
          placeholder = "Enter TODO"
          placeholderTextColor = "black"
          onChangeText={this.takeInput}
          value={this.state.text}
        />
        <Button onPress={() => this.addTodo(this.state.text)} title="Add TODO" color="black" />
        <ScrollView style={styles.fill}>
          {this.state.todos.map(todo => (
            <Todo
              onToggle={() => this.toggleTodo(todo.id)}
              onDelete={() => this.removeTodo(todo.id)}
              todo={todo}
            />
          ))}
        </ScrollView>
      </View>
    )
  }
}

